from ast import Module
import datetime
import secrets
from unittest import case
from django.http import JsonResponse
from django.shortcuts import render,get_object_or_404,redirect,HttpResponse
from .models import Category,Course,Module,ModuleTitle,CourseDetail, ModuleTitle,Result,QuizAnswer,QuizQuestion, CourseMaterial, StudentExamAssociation,Subscription,Enrollment, CourseNote,ContactUs,CourselImage,CoursePdf, Question,Answer,UpVote,DownVote, UserCourseEnrollment,UserProfile,Quiz
from django.contrib.auth.models import User
from django.db.models import Count,Exists, OuterRef
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView
from django.db.models import Max

from django.http import JsonResponse
# from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.contrib import messages
# for padf generator
from eduapp.utils import render_to_pdf
from django.views.generic import View

# email
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from core.settings import EMAIL_HOST_USER

# certificate
from reportlab.pdfgen import canvas
from io import BytesIO
from reportlab.lib.pagesizes import A4,letter,landscape
from reportlab.pdfgen import canvas

# Payment 
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from .paytm import checksum
from .paytm.checksum import verify_checksum

from core.settings import MERCHANT_KEY,MID

MERCHANT_KEY = MERCHANT_KEY


from .forms import CreateUserForm,AnswerForm, QuestionsForm, QuizCreationForm

# Create your views here.
class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        data={
            "name":"dhanashree",
            "course":"python"
        }
        pdf = render_to_pdf('invoice.html',data)
        return HttpResponse(pdf, content_type='application/pdf')
    
def pdf(request):
    return render(request,"invoice.html")

def email(request):
    return render(request,"email_temp.html")

def categories(request):
    return{
        'categories':Category.objects.all()
    }

def products(request):
    return{
        'products':Course.objects.all()
    }

def contact(request):
    if request.method=="POST":
        name=request.POST.get("name")
        email=request.POST.get("email")
        msg=request.POST.get("msg")
        phone=request.POST.get("phone")
        course=request.POST.get("course")
        ContactUs.objects.create(name=name,email=email,msg=msg,phone=phone,course=course)
        context={"name":name}
        html_message = render_to_string('email_temp.html')
        if course and email:
            try:
                send_mail('Thanks for contacting Us', "welcome",EMAIL_HOST_USER, [email],html_message=html_message,)
            except BadHeaderError:
                return HttpResponse("Invalid header found.")
        return render(request,"forms/conform/conformation.html",{'name':name,'product_details':course})
    return render(request,"forms/contact_us.html")

def home(request):
    courselImage=CourselImage.objects.all()
    cat=Category.objects.all()
    return render(request,"home.html",{"courselImage":courselImage,"cat":cat})


def course_view(request,category_slug):
    
    category=get_object_or_404(Category,slug=category_slug)
    product=Course.objects.filter(category=category)
    return render(request,'product.html',{'product':product})

def course_details(request,slug):

    product=get_object_or_404(Course,slug=slug)
    product_details=CourseDetail.objects.filter(product=product).first()
    if product_details is None:
        return redirect(soon)
    return render(request,'product_details.html',{'product_details':product_details})
    # else:
    #     return render(request,'product_details.html')


def enrollmentForm(request,id):
    quali=["SSC","HSC","undergraduate","Graduate","Postgraduate"]
    if request.user.is_authenticated:
        
        if id:
            product_detail=CourseDetail.objects.get(id=id)
            product_details=product_detail
        if request.method=="POST":
            username=request.user.username
            fname=request.POST.get('f-name')
            mname=request.POST.get('m-name')
            lname=request.POST.get('l-name')
            email=request.POST.get('email')
            dob=request.POST.get('dob')
            address=request.POST.get('address')
            nationality=request.POST.get('nationality')
            gender=request.POST.get('gender')
            phone=request.POST.get('phone')
            qualification=request.POST.get('qauli')
            exp=request.POST.get('exp')
            course=request.POST.get('course')
            duration=request.POST.get('duration')
            documents=request.FILES.get('documents')
            user_profile, created = UserProfile.objects.get_or_create(user=request.user)
            if documents:
                user_profile.documents = documents
            user_profile.experience = exp
            user_profile.date_of_birth= dob
            user_profile. gender=gender
            user_profile.educational_qualification =qualification
            user_profile.phone_number=phone
            user_profile.nationality=nationality
            user_profile.address=address
            # Update other fields as needed
            user_profile.save()
            selected_course_id = request.POST.get('course')
            selected_course = Course.objects.get(name=selected_course_id)

            # Create an enrollment instance for the user and the selected course
            user_profile = UserProfile.objects.get(user=request.user)
            enrollment = Enrollment.objects.create(
            user_profile=user_profile,
            course=selected_course,
            training_timings=duration,
        )


            subject = f'Welcome to {course}! Complete Your Enrollment by Finalizing Payment'
            context = {
                'fname': fname,
                'course': course,
                'website_url': "abc.com",
                'course_name': course,
                'support_email': EMAIL_HOST_USER,
                'support_phone_number': "24534657",
                'your_name': "Instructor",
                'your_title': "instructer",
            }

            html_message = render_to_string('email_templates/course_enrollment.html', context)
            plain_message = strip_tags(html_message)
            if course and email:
                try:
                    send_mail(subject, plain_message,EMAIL_HOST_USER, [email],html_message=html_message)
                except BadHeaderError:
                    return HttpResponse("Invalid header found.")
            #coursePdf=CoursePdf.objects.get(name=course) 
            courseid=Course.objects.get(name=course).price 
            param_dict = {

                'MID': MID,
                'ORDER_ID': str( enrollment.order_id),
                'TXN_AMOUNT':'1',
                'CUST_ID':email ,
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'DEFAULT',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL':'http://127.0.0.1:8000/handlerequest/',

            }
            param_dict['CHECKSUMHASH'] = checksum.generate_checksum(param_dict, MERCHANT_KEY)
           
            return render(request,"forms/payment/paytm.html",{"param_dict":param_dict})
        
            # return render(request,"forms/conform/conformation.html",{'name':fname,'product_details':product_details,"pdf":coursePdf})
        userinfo=UserProfile.objects.get(user=request.user)    
        return render(request,"forms/admission.html",{'product_detail':product_details,'quali':quali,"userinfo":userinfo})
    else:
        messages.success(request,("Required to Login"))
        return redirect("login")

def searchresultsview(request):
    if request.method=="GET":
        query = request.GET.get("q")
        object_list =Course.objects.filter(name__icontains=query) or Category.objects.filter(name__icontains=query)
        return render(request,"search_result.html",{'object_list':object_list})
    return render(request,"search_result.html")
    

def conform(request):
    return render(request,"forms/conform/conformation.html")

def login(request):
    if request.method=="POST":
        username=request.POST["username"]
        password=request.POST["pass"]
        user=authenticate(request,username=username,password=password)
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        if user is not None:
            auth_login(request,user)
            if request.user.is_superuser: 
                return redirect(TrainerDashboard)
            redirect_url = request.GET.get('next','')
            print(redirect_url)
            return redirect(redirect_url) if redirect_url else redirect('home')
        else:
            messages.success(request,("Incorrect Username or Passowrd"))
            return redirect("login")
    return render(request,"forms/login.html")

def register(request):

    if request.method=="POST":
        form=CreateUserForm(request.POST)
        if form.is_valid():
            if User.objects.filter(username=form.cleaned_data['username']).exists():
                return render(request,'forms/signup.html', {
                    'form': form,
                    'error_message': 'Username already exists.'
                })
            elif User.objects.filter(email=form.cleaned_data['email']).exists():
                return render(request,'forms/signup.html', {
                    'form': form,
                    'error_message': 'Email already exists.'
                })
            elif form.cleaned_data['password'] != form.cleaned_data['password_repeat']:
                return render(request,'forms/signup.html', {
                    'form': form,
                    'error_message': 'Passwords do not match.'
                })
            else:
                email=form.cleaned_data['email']
                username=form.cleaned_data['username']
                first_name=form.cleaned_data['first_name']
                # Create the user:
                user = User.objects.create_user(
                    username=form.cleaned_data['username'],
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password']
                )
                user.save()
                today=datetime.datetime.today()
                subject = "Welcome to [Company/Organization Name]! Your Registration is Complete"
                context = {
                    'username': username,
                    'email': email,
                    'today': today,
                }
                user.backend = 'django.contrib.auth.backends.ModelBackend'

                # Plain text version
                
                html_message = render_to_string('email_templates/registration_complete_email.html', context)
                plain_message = strip_tags(html_message)

  
                if email:
                    try:
                        send_mail('Welcome to Our Website', plain_message,EMAIL_HOST_USER, [email],html_message=html_message,)
                    except BadHeaderError:
                        return HttpResponse("Invalid header found.")
                # Login the user
                auth_login(request, user)
                return redirect("home")
               
    form=CreateUserForm()
    return render(request,'forms/signup.html',{"form":form})

def Profile(request):
    return render(request,"profile/trainerProfile.html")

@method_decorator(login_required, name='dispatch')
class QuizListView(ListView):
    model = Quiz
    template_name = 'dashboard/Quizes/main.html'

    context_object_name = 'quizzes'

    def get_queryset(self):
        # Get the current user
        current_user = self.request.user

        # Get the list of quizzes that the current user is associated with
        student_associations = StudentExamAssociation.objects.filter(student=current_user)

        # Get the primary keys of the quizzes associated with the current user
        quiz_ids = student_associations.values_list('exam__pk', flat=True)

        # Filter quizzes by the provided module_title_id if it exists
        module_title_id = self.request.GET.get('module_title_id')
        if module_title_id:
            return Quiz.objects.filter(pk__in=quiz_ids, topic__pk=module_title_id)
        else:
            return Quiz.objects.filter(pk__in=quiz_ids)

def quiz_view(request,pk):
    quiz=Quiz.objects.get(pk=pk)
    return render(request,'dashboard/Quizes/Quiz.html',{'obj':quiz})

def quiz_data_view(request,pk):
    quiz=Quiz.objects.get(pk=pk)
    question=[]
    for q in quiz.get_questions():
        answers=[]
        for a in q.get_answers():
            answers.append(a.text)
        question.append({str(q):answers})
    return JsonResponse({'data':question,
                        'time':quiz.time})
def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def save_quiz_view(request,pk):
    # print(request.POST)
    if is_ajax(request=request):
        questions=[]
        data=request.POST
        data_=dict(data.lists())
        data_.pop('csrfmiddlewaretoken')
        for k in data_.keys():
            print('key:',k)
            
            question = QuizQuestion.objects.filter(text=k).first()
            if question:
                questions.append(question)   
            else:
                print(f"Question with text '{k}' does not exist in the database.")
        print(questions)
        user=request.user
        quiz=Quiz.objects.get(pk=pk)

        score=0
        multiplier=100/quiz.number_of_questions
        results=[]
        correct_answer=None

        for q in questions:
            a_selected=request.POST.get(q.text)
            
            if a_selected!="":
                question_answers=QuizAnswer.objects.filter(question=q)

                for a in question_answers:
                    if a_selected==a.text:
                        if a.correct:
                            score+=1
                            correct_answer=a.text
                    else:
                        if a.correct:
                            correct_answer=a.text
                results.append({str(q):{'correct_answer':correct_answer,"answered":a_selected}})
            else:
                results.append({str(q):'not_answered'})
        
        score_ = 0

        if score > 0:
            score_ = float(score * multiplier)
                
        Result.objects.create(quiz=quiz,user=user,score=score_)
        Submit=StudentExamAssociation.objects.get(Q(exam=quiz) and Q(student=request.user))
        Submit.submitted=True
        Submit.save()

        if score_>=quiz.required_score_to_pass:
            return JsonResponse({'passed':True,'score':score_,'result':results})
        else:
            return JsonResponse({'passed':False,'score':score_,'result':results})
        

def create_quiz(request):
    categories = Category.objects.all()
    courses = []
    modules = []
    submodules = []

    selected_category = request.GET.get('category')
    selected_course = request.GET.get('course')
    selected_module = request.GET.get('module')

    if selected_category:
        courses = Course.objects.filter(category=selected_category)
        print(courses)

    if selected_course:
        modules = Module.objects.filter(course_id=selected_course)

    if selected_module:
        submodules =ModuleTitle.objects.filter(module_id=selected_module)

    if request.method == 'POST':
        form = QuizCreationForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.submodule_id = request.POST.get('submodule')
            quiz.save()
            return JsonResponse({'message': 'Quiz created successfully'})
        else:
            return JsonResponse({'error': 'Form validation failed'})

    return render(request, 'trainerDashboard/quiz_admin/create_quiz.html', {
        'categories': categories,
        'courses': courses,
        'modules': modules,
        'submodules': submodules,
    })

def generate_token():
    return secrets.token_urlsafe(32)

def send_subscription_email(user, token):
    subject = "Confirm Subscription"
    message = f"Click the link to confirm your subscription:  http://127.0.0.1:8000/confirm-subscription/{token}/"
    from_email = "your@email.com"
    recipient_list = [user.email]

    send_mail(subject, message, from_email, recipient_list)
# def unsubscribe_view(request):
#     # Update the user's subscription status and send confirmation email
#     subscription = Subscription.objects.get(user=request.user)
#     subscription.subscribed = False
#     subscription.save()
#     send_subscription_email(request.user, token)
#     return render(request, 'subscription/confirmation.html')


# def payment(request,pk):
#     if request.user.is_authenticated:
#         if request.method=="POST":
#             name=request.user.first_name
#             email=request.user.email
#             course=Course.objects.get(id=pk).name
#             trans_id=request.POST["transid"]
#             Payment.objects.create(email=email,student=name,course=course,upiTransactionNum=trans_id)
#             coursePdf=CoursePdf.objects.get(name=course)
#             context = {
#                     'username': name,
#                     'email': email,
#                     'course':course
#                 }

#                 # Plain text version
#             html_message = render_to_string('email_templates/registration_complete_email.html', context)
#             plain_message = strip_tags(html_message)



#             if course and email:
#                 try:
#                     send_mail(f'Thank You for Enrolling in [Course Name]! Next Steps and Payment Verification',plain_message,EMAIL_HOST_USER, [email],html_message=html_message)
#                 except BadHeaderError:
#                     return HttpResponse("Invalid header found.")
#             return render(request,"forms/conform/conformation.html",{'name':name,"pdf":coursePdf,"course":course})
#     return render(request,"forms/payment/payment.html")

@csrf_exempt
def handlerequest(request):
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
            try:
                order_id = response_dict['ORDERID']  # Use the correct key name
                enrollment = Enrollment.objects.get(order_id=order_id)
                enrollment.payment_status = 'SUCCESS'
                enrollment.save()
                context={
                    "enrollment":enrollment,
                    "response_dict":response_dict

                }
                html_message = render_to_string('email_templates/payment_email.html', context)
                plain_message = strip_tags(html_message)
                subject="Confirmation of Successful Payment for Course Enrollment"
                send_mail(subject, plain_message,EMAIL_HOST_USER, [enrollment.user_profile.user.email],html_message=html_message)
                

            except:
                pass
            
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'forms/payment/paymentstatus.html', {'response': response_dict})


def soon(request):
    return render(request,"forms/conform/comingsoon.html")

def displayQuestions(request):
    questions_with_answer_counts = Question.objects.annotate(num_answers=Count('answer'))
    return render(request,"Que/displayQuestion.html",{'questions_with_answer_counts': questions_with_answer_counts})



def displayAnswer(request,id):
    if request.user.is_authenticated:
        answers = Answer.objects.filter(question=id).annotate(num_upvote=Count('upvote'),
                                user_has_upvoted=Exists(UpVote.objects.filter(answer_id=OuterRef('id'), student=request.user)
            ))
        return render(request,"Que/showAnswers.html",{"answers":answers})
    

def answer(request,id):
    que=Question.objects.get(id=id)
    form=AnswerForm()
    if request.method=="POST":
        form=AnswerForm(request.POST)
        if form.is_valid():
            ques=form.save(commit=False)
            ques.student=request.user
            ques.question=que
            ques.save()
            answer=form.cleaned_data["ans"]
            users=User.objects.all()
            for user in users:
                if user==que.student:
                    plain_text_answer = strip_tags(answer)
                    plain_que=strip_tags(que.query)
                    messages=f'''hello {user.username},
                    qusetion : {plain_que} 
                    answer given by {request.user}
                    Answer: {plain_text_answer}'''
                    subject="Someone answered your question - Check if it was helpful"
                    send_mail(subject, messages,EMAIL_HOST_USER, [user.email])

            return redirect("displayQuestions")
    return render(request,"Que/answer.html",{"form":form,"que":que})

def questionView(request):
    form=QuestionsForm()
    if request.method=="POST":
        form=QuestionsForm(request.POST)
        if form.is_valid():
            # print("valid")
            ques=form.save(commit=False)
            ques.student=request.user
            ques.save()
            question=form.cleaned_data["query"]
            users=User.objects.all()
            for user in users:
                plain_que=strip_tags(question)
                if user!=request.user:
                    messages=f'''hello {user.username},
                    qusetion is {plain_que}'''
                    subject="New Question is posted by someone see if you can answer it."
                    send_mail(subject, messages,EMAIL_HOST_USER, [user.email])
                else:
                    messages=f'''hello {user.username},
                    qusetion is {plain_que}'''
                    subject="Your question is posted successfully."
                    send_mail(subject, messages,EMAIL_HOST_USER, [user.email])
                    


            return redirect("displayQuestions")
    return render(request,"Que/question.html",{"form":form})


def upvote_answer(request):
    if request.method == "POST" and request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest":
        answer_id = request.POST.get("answer_id")
        try:
            answer = Answer.objects.get(pk=answer_id)
            user_has_upvoted = UpVote.objects.filter(answer=answer, student=request.user).exists()

            if user_has_upvoted:
                UpVote.objects.filter(answer=answer, student=request.user).delete()
            else:
                UpVote.objects.create(answer=answer, student=request.user)

            upvote_count = UpVote.objects.filter(answer=answer).count()
            return JsonResponse({"upvote_count": upvote_count, "upvoted": not user_has_upvoted})
        except Answer.DoesNotExist:
            return JsonResponse({"error": "Answer not found"}, status=400)
    return JsonResponse({"error": "Invalid request"}, status=400)

def questionSearchResults(request):
    if request.method=="GET":
        query = request.GET.get('que')
        if query:
            questions = Question.objects.filter(query__icontains=query).annotate(num_answers=Count('answer'))
            return render(request,"searchQue.html" ,{"quesAns":questions})
        else:
            questions = Question.objects.none()
            return redirect("displayQuestions")

def dashboard(request):
    user = request.user
    try:
        userprof=UserProfile.objects.get(user=user)
        enrolled_courses = Enrollment.objects.filter(user_profile=userprof,payment_status="SUCCESS")
        return render(request, 'dashboard/course_dashboard.html', {
        'enrolled_courses':enrolled_courses
    })
    except:
        return render(request, 'dashboard/course_dashboard.html')
    if request.user.is_superuser: 
        return redirect(TrainerDashboard)
    
    # enrolled_courses = UserCourseEnrollment.objects.filter(user=user).values('course')
    # 
   
def TrainerDashboard(request):
    if request.user.is_superuser: 
        enrolled_students = UserCourseEnrollment.objects.all()
        return render(request,"TrainersDashboard.html",{"enrolled_students":enrolled_students})

def TrainerCourseMaterial(request):
    courses=Course.objects.all()
    courseMaterial=CourseMaterial.objects.all()

    if request.method == "POST":
        course_name = request.POST.get("courses")
        material = request.FILES.get("document")

        try:
            course = Course.objects.get(Q(name__iexact=course_name))
            CourseMaterial.objects.create(course=course, courseFile=material)
            msg = "Uploaded successfully"
        except ObjectDoesNotExist:
            msg = "Course not found"
        return render(request, "trainerDashboard/trainerCourseMaterial.html", {"courses": courses,"courseMaterials":courseMaterial,"msg": msg})

    return render(request, "trainerDashboard/trainerCourseMaterial.html", {"courses": courses,"courseMaterials":courseMaterial})

def course_material(request,id):
    enrolled_course=Course.objects.get(id=id)
    course_notes = CourseMaterial.objects.filter(course=enrolled_course)

    return render(request,'dashboard/course_material.html',{"course_notes":course_notes})
 
def userProfile(request):
    quali = ["SSC", "HSC", "undergraduate", "Graduate", "Postgraduate"]
    if request.user.is_authenticated:
        user = request.user
        user_profile, created = UserProfile.objects.get_or_create(user=user)

        if request.method == "POST":
            nation = request.POST.get('nationality')
            dob = request.POST.get("inputBirthday")
            doc = request.FILES.get('documents')
            exp = request.POST.get('inputexp')
            edu = request.POST.get('qauli')
            phone = request.POST.get('inputPhone')
            add = request.POST.get('inputLocation')

            if add:
                user_profile.address = add
            if phone:
                user_profile.phone_number = phone
            if edu:
                user_profile.educational_qualification = edu
            if nation:
                user_profile.nationality = nation
            if exp:
                user_profile.experience = exp
            if dob:
                user_profile.date_of_birth = dob
            if doc:
                user_profile.documents = doc

            # Save changes
            user_profile.save()
            user_profile.user.save()

    return render(request, 'dashboard/profile.html', {"quali": quali, "profile": user_profile})
def upload_quiz(request):
    return render(request,"trainerDashboard/upload_quiz.html")

def notes(request):
    if request.user.is_authenticated:
        return render(request,'dashboard/notes.html')
def tests(request):
    if request.user.is_authenticated:
        user = request.user
        result = Result.objects.filter(user=user)
        max_score = result.aggregate(Max('score'))['score__max']
        # latest_quiz = Quiz.objects.latest('created')
        # print(latest_quiz)

        try:
            userprof = UserProfile.objects.get(user=user)
            enrolled_courses = Enrollment.objects.filter(user_profile=userprof, payment_status="SUCCESS")
            topics = []

            for enrolled_course in enrolled_courses:
                course = enrolled_course.course
                course_obj = Course.objects.get(name=course)
                course_topics = Module.objects.filter(course=course_obj)
                
                # Extend the topics list with the topics of the current course
                topics.extend(course_topics)

            # Now 'topics' should contain all the topics/modules for the enrolled courses
            print(topics)
            # Now 'topics' should contain all the topics/modules for the enrolled courses
            # To retrieve all module titles under all modules, you can do this:
            module_titles = ModuleTitle.objects.filter(module__in=topics)
            for title in module_titles:
                print(title.title)
                context={
                    'max_score':max_score,
                    'Topics':module_titles,
                    # 'latest_quiz':latest_quiz
                    

                }


            return render(request,'dashboard/test.html',context)
        except:

            return render(request,'dashboard/test.html',{'max_score':max_score})
    
   
       

def moduleTitle(request, module_id):
    module = get_object_or_404(Module, pk=module_id)

    if request.method == 'POST':
        title_text = request.POST.get('title', '')  # Assuming your form input name is 'title'
        module_title = ModuleTitle.objects.create(module=module, title=title_text)
        # You can add further logic here, like validation or redirection after creation.
        return redirect('all_module_data')
    return render(request, 'trainer_dashboard/moduleTitle.html', {'module': module})

# def pdfgenerator(request,id):
#     student=Admission.objects.get(id=id)
#     response = HttpResponse(content_type = 'application/pdf')
#     response['Content-Disposition'] = 'filename="Bill.pdf"'
#     buffer = BytesIO()
#     p = canvas.Canvas(buffer, pagesize=landscape(letter))
#     letter_head = "./eduapp/document/CERTIFICATE_page-0001.jpg"
#     p.drawImage(letter_head,0,0,width=790,height=650)
#     p.setFont("Helvetica", 30)
#     p.drawString(320, 400,student.firstname+" "+student.lastname)
#     p.drawString(320, 200,student.duration)
#     p.showPage
#     p.save()
#     p = buffer.getvalue()
#     buffer.close()
#     response.write(p)
#     return response


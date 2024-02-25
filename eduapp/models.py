from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
import random

boolchoices=[
    ("yes","yes"),
    ("no","no")
]


# Create your models here.
class CourselImage(models.Model):
    title=models.CharField(max_length=255,default="")
    sub_title=models.TextField(default="")
    button_name=models.CharField(max_length=255,default="")
    image=models.ImageField(upload_to="eduapp/coursel")
    def __str__(self):
        return self.title

class Trainer(models.Model):
    name=models.CharField(max_length=255)
    description=models.TextField()
    profile_pic=models.ImageField(upload_to="trainer/",default=None)

    
class Category(models.Model):
    name=models.CharField(max_length=100)
    image=models.ImageField(upload_to='eduapp/images/category')
    slug=models.SlugField(max_length=255,unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural='categories'

    def get_absolute_url(self):
        return reverse('course_view',args=[self.slug])

class Level(models.Model):
    level=models.CharField(max_length=255)

class Course(models.Model):
    name=models.CharField(max_length=100)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    price=models.IntegerField(null=True,default=0)
    image=models.ImageField(upload_to='eduapp/images/product')
    slug=models.SlugField(max_length=255,unique=True)
    author=models.ForeignKey(Trainer,on_delete=models.CASCADE,null=True)
    discount=models.IntegerField(null=True)
    created_at=models.DateField(auto_now_add=True,null=True)
    level=models.ForeignKey(Level,on_delete=models.CASCADE,null=True)


    class Meta:
        verbose_name_plural='Courses'
  

    def get_absolute_url(self):
        return reverse('course_details',args=[self.slug])


    def __str__(self):
        return self.name
    
class Duration(models.Model):
    duration=models.TextField()

    def __str__(self):
        return self.duration

class CourseDetail(models.Model):
    product=models.OneToOneField(Course,on_delete=models.CASCADE)
    description=RichTextField()
    duration=models.ForeignKey(Duration,null=True,on_delete=models.DO_NOTHING)
    startdate=models.DateField()
    requirements=RichTextField(default="")
    topics=RichTextField(default="")
    lecture=models.CharField(max_length=255)
    assignment=models.CharField(max_length=50,choices=boolchoices)
    test=models.CharField(max_length=50,choices=boolchoices)

    

# class Video(models.Model):
#     sr_no=models.IntegerField(null=True)
#     thumbnail=models.ImageField(upload_to="youtube/")

class ContactUs(models.Model):
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    msg=models.TextField()
    phone=models.CharField(max_length=12)
    course=models.CharField(max_length=255)

    class Meta:
        verbose_name_plural='Contacts'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    documents = models.FileField(upload_to="student/documents/")
    educational_qualification = models.CharField(max_length=100)
    experience = models.TextField()
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=20)
    nationality = models.CharField(max_length=100)
    address=models.TextField(default=""),


    def __str__(self):
        return self.user.username
    
class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscribed = models.BooleanField(default=True)

class Enrollment(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrollment_date = models.DateTimeField(auto_now_add=True)
    training_timings = models.CharField(max_length=255)
    order_id = models.AutoField(primary_key=True)
    payment_status=models.CharField(max_length=255,default="fail")
    
 
class CoursePdf(models.Model):
    name=models.CharField(max_length=255)
    pdf=models.FileField(upload_to='eduapp/coursepdf/')

    def __str__(self):
        return self.name

class Question(models.Model):
    student=models.ForeignKey(User,on_delete=models.CASCADE)
    query=RichTextField()
    created_date=models.DateField(auto_now_add=True)


class Answer(models.Model):
    student=models.ForeignKey(User,on_delete=models.CASCADE)
    question=models.ForeignKey(Question,on_delete=models.CASCADE)
    ans=RichTextField()
    created_date=models.DateField(auto_now_add=True)

class Comment(models.Model):
    answer=models.ForeignKey(Answer,on_delete=models.CASCADE)
    student=models.ForeignKey(User,on_delete=models.CASCADE)
    comment=RichTextField()
    created_date=models.DateField(auto_now_add=True)

class UpVote(models.Model):
    answer=models.ForeignKey(Answer,on_delete=models.CASCADE)
    student=models.ForeignKey(User,on_delete=models.CASCADE)


class DownVote(models.Model):
    answer=models.ForeignKey(Answer,on_delete=models.CASCADE)
    student=models.ForeignKey(User,on_delete=models.CASCADE)

class CourseNote(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()    

class UserCourseEnrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
   

    class Meta:
        unique_together = ('user', 'course')

class CourseMaterial(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    courseFile=models.FileField(upload_to='eduapp/coursepdf/')

class Module(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    module=models.CharField(max_length=300)

class ModuleTitle(models.Model):
    module=models.ForeignKey(Module,on_delete=models.CASCADE)
    title=models.TextField()

class Quiz(models.Model):
    name=models.CharField(max_length=120)
    topic=models.ForeignKey(ModuleTitle,on_delete=models.CASCADE)
    number_of_questions=models.IntegerField()
    time=models.IntegerField(help_text="duration of the quiz in minutes")
    required_score_to_pass=models.IntegerField(help_text="required score to pass")
    students = models.ManyToManyField(User, through='StudentExamAssociation', related_name='exams')

    def __str__(self):
        return f"{self.name}-{self.topic.title}"
    
    def get_questions(self):
        questions=list(self.quizquestion_set.all())
        random.shuffle(questions)
        return questions[:self.number_of_questions]

class QuizQuestion(models.Model):
    text=RichTextField()
    quiz=models.ForeignKey(Quiz,on_delete=Quiz)
    created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.text)
    def get_answers(self):
        return self.quizanswer_set.all()

class QuizAnswer(models.Model):
    text=RichTextField()
    correct=models.BooleanField(default=False)
    question=models.ForeignKey(QuizQuestion,on_delete=models.CASCADE)
    created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"questions:{self.question.text}, answer:{self.text}, correct:{self.correct}"

class Result(models.Model):
    quiz=models.ForeignKey(Quiz,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    score=models.FloatField()

    def __str__(self
                ):
        return self.pk
    
class StudentExamAssociation(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)  # Assuming you're using the User model for students
    exam = models.ForeignKey(Quiz, on_delete=models.CASCADE)  # Replace Exam with your actual Exam model
    is_allowed = models.BooleanField(default=False)  # Indicates whether the student is allowed for the exam
    submitted = models.BooleanField(default=False) 


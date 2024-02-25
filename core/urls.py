from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from eduapp import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from eduapp.views import *
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("admin/", admin.site.urls),
    path('accounts/', include('allauth.urls')), 
    path('ckeditor/',include('ckeditor_uploader.urls')),
    path("contact/",views.contact,name="contact"),
    path("",views.home,name="home"),
    path("search/", views.searchresultsview, name="search_results"),
    path("course/<slug:category_slug>",views.course_view,name="course_view"),
    path("course_details/<slug:slug>",views.course_details,name="course_details"),
    path("enrollmentform/<int:id>",views.enrollmentForm,name="enrollmentForm"),
    path('conformation/',views.conform,name="conform"),
    path('login/',views.login,name='login'),
    path('register',views.register,name='register'),
    path('trainerProfile',views.Profile,name="profile"),
    # path("payment/<int:pk>",views.payment,name="payment"),
    path("coomingsoon/",views.soon,name="soon"),
    path("logout/",LogoutView.as_view(),name="logout"),
    path("email/",views.email,name="email"),
    path("dashboard/",views.dashboard,name="dashboard"),
    path("user-profile/",views.userProfile,name="userProfile"),
    path("course_material/<int:id>",views.course_material,name="course_material"),
    path("dashboard/notes",views.notes,name="notes"),
    path("dashboard/tests",views.tests,name="tests"),
    path("trainer-dashboard/",views.TrainerDashboard,name="trainer_dashboard"),
    path("trainer-dashboard/course-material",views.TrainerCourseMaterial,name="TrainerCourseMaterial"),
    path("trainer-dashboard/upload_quiz",views.upload_quiz,name="upload_quiz"),
    path("handlerequest/",views.handlerequest,name="handlerequest"),

    #admi-Quiz-creation urls
    path('trainer-dashboard/create-quiz',views.create_quiz,name="trainer-create-quiz"),
    
    #Quiz urls
    path("dashboard/quiz/",QuizListView.as_view(),name="quiz-list"),
    path("dashboard/quiz/<int:module_title_id>",QuizListView.as_view(),name="quiz-list-module-title"),
    path('dashboard/quiz/<pk>/',views.quiz_view,name='quiz-view'),
    path('dashboard/quiz/<pk>/data/',views.quiz_data_view,name='quiz-data-view'),
    path('dashboard/quiz/<pk>/save/',views.save_quiz_view,name='quiz-save'),


    # path("pdfgenerator/",GeneratePdf.as_view(),name="pdfgenerator"),
    # path('unsubscribe/', views.unsubscribe_view, name='unsubscribe'),
    path("pdf/",views.pdf,name="pdf"),
    path("display-question/",views.displayQuestions,name="displayQuestions"),
    path("question/answer/<int:id>",views.answer,name="answer"),
    path("question/",views.questionView,name="question"),
    path("answers/<int:id>",views.displayAnswer,name="displayAnswer"),
    path('upvote-answer/', views.upvote_answer, name='upvote_answer'),
    # path('pdfgenerator/<int:id>',views.pdfgenerator,name='pdfgenerator'),
    path('question-search/',views.questionSearchResults,name='questionSearchResults'),
    #password reset paths
    path('password_reset/',auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),

    
    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
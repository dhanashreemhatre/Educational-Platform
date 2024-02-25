from django.contrib import admin,messages
from eduapp.models import Category,Course,CourseDetail,StudentExamAssociation,Duration,CourselImage,Level,Enrollment,Question,UpVote,DownVote,Comment,Answer,CoursePdf,ContactUs,UserCourseEnrollment,CourseNote,UserProfile,CourseMaterial,Trainer,Quiz,Module,ModuleTitle,QuizAnswer,QuizQuestion,Result

# Register your models here.
@admin.register(Category)
class categoryadmin(admin.ModelAdmin):
    list_display=('name','image')
    prepopulated_fields={'slug':('name',)}

@admin.register(Course)
class productadmin(admin.ModelAdmin):
    list_display=('name','category','price','image',)
    prepopulated_fields={'slug':('name',)}

@admin.register(CourseDetail)
class productdetailsadmin(admin.ModelAdmin):
    list_display=('product','description','duration')

@admin.register(ContactUs)
class ContactusAdmin(admin.ModelAdmin):
    list_display=('name','email',)

@admin.register(CourselImage)
class CourselImgAdmin(admin.ModelAdmin):
    list_display=('image','title')


@admin.register(CoursePdf)
class CoursepdfAdmin(admin.ModelAdmin):
    list_display=('name',)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display=('student','query',)

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display=('student','question',)

@admin.register(UpVote)
class QuestionAdmin(admin.ModelAdmin):
    list_display=('student',)

@admin.register(UserCourseEnrollment)
class UserCourseEnrollmentAdmin(admin.ModelAdmin):
    list_display=("user","course",)

@admin.register(CourseNote)
class CourseNoteAdmin(admin.ModelAdmin):
    list_display=("title","course",)

admin.site.register(UserProfile)

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display=("enrollment_date",)

admin.site.register(CourseMaterial)
admin.site.register(Trainer)
admin.site.register(Level)
admin.site.register(Duration)
admin.site.register(Module)
admin.site.register(ModuleTitle)
admin.site.register(Quiz)
class AnswerInline(admin.TabularInline):
    model=QuizAnswer

class QuestionAdmin(admin.ModelAdmin):
    inlines=[AnswerInline]

admin.site.register(QuizQuestion,QuestionAdmin)
admin.site.register(QuizAnswer)
    
def allow_students(modeladmin, request, queryset):
    queryset.update(is_allowed=True)
    messages.success(request, "Selected students have been allowed for the exam.")

def disallow_students(modeladmin, request, queryset):
    queryset.update(is_allowed=False)
    messages.success(request, "Selected students have been disallowed for the exam.")

allow_students.short_description = "Allow selected students for the exam"
disallow_students.short_description = "Disallow selected students for the exam"

@admin.register(StudentExamAssociation)
class StudentExamAssociationAdmin(admin.ModelAdmin):
    list_display = ('student', 'exam', 'is_allowed')
    actions = [allow_students, disallow_students]
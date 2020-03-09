from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import slugify
from django.utils import timezone

from .managers import CustomUserManager

# Character model
class Character(models.Model):
    characterType = models.IntegerField(_("type"),default=1)
    evolutionStage = models.IntegerField(_("stage"),default=1)
    evolveScore = models.IntegerField(_("score"),default=0)

    def __str__(self):
        return str(self.characterType)

# User model
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_("user name"), max_length=50, unique=True)
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(_("name"), max_length=50)
    is_admin = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    character = models.ForeignKey("Character", blank=True, null=True, on_delete=models.SET_NULL)

    #Required django User fields
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    #####

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Class(models.Model):
    classId = models.AutoField(primary_key=True,verbose_name=_("id"))
    name = models.CharField(_("name"), max_length=50)
    teacher = models.ManyToManyField("User", verbose_name=_("teacher"),related_name="teachers")
    student = models.ManyToManyField("User", verbose_name=_("student"),related_name="students")

    def get_teachers(self):
        return ",".join([str(t) for t in self.teacher.all()])

    def get_students(self):
        return ",".join([str(s) for s in self.student.all()])

    def __str__(self):
        return self.name

    class Meta:
        # Fix pluralization of model name
        verbose_name_plural = 'Classes'

# Quiz Model
class Quiz(models.Model):
    name = models.CharField(unique=True, max_length=50)
    # Course represents class model
    course = models.ManyToManyField(Class)
    description = models.CharField(max_length=255)
    due_date = models.DateTimeField(auto_now_add=False)
    question_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        # Fix pluralization of model name
        verbose_name_plural = 'Quizzes'

# Question model
class Question(models.Model):
    text = models.CharField(unique=True, max_length=50)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

# Option Model
class Option(models.Model):
    text = models.CharField(unique=True, max_length=50)
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

# QuizTaker model
class QuizTaker(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    correctAnswers = models.IntegerField(default=0)
    is_completed = models.BooleanField(default=False)
    timestamp = models.DateTimeField()

    def __str__(self):
        return self.user

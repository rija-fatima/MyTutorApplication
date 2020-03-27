import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    # username = None
    role = models.CharField(max_length=12, error_messages={
        'required': "Role must be provided"
    })
    email = models.EmailField(unique=True, blank=False,
                              error_messages={
                                  'unique': "A user with that email already exists.",
                              })

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __unicode__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    education = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="profiles/", default="profiles/avatar.png")

    def __str__(self):
        return "Profile of {}".format(self.user.username)


@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    print(created)
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class Subject(models.Model):
    subject = models.CharField(max_length=128)
    subject_url = models.URLField()
    # dont know if cascade is what it should be
    tutor = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.subject


class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    credit = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class CourseTeacher(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="my_courses")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="course_teachers")

    def __str__(self):
        return "{} is teacher of course {}".format(self.teacher.username, self.course.title)


class Comment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content


class Booking(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="my_students")
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="my_teachers")
    is_accepted = models.BooleanField(default=False)
    date = models.DateField()
    time = models.TimeField()


class EnrolledCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

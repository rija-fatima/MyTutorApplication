from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from mytutor.forms import *
from mytutor.models import *


def index(request):
    context_dict = {'boldmessage': 'here is the home page'}
    return render(request, 'mytutor/index.html', context=context_dict)


def browsecourse(request):
    context_dict = {}
    courses = Course.objects.all()
    context_dict["courses"] = courses
    return render(request, 'mytutor/browse_course.html', context=context_dict)


def course_details(request, id):
    course = Course.objects.prefetch_related("comment_set__user").get(id=id)
    course_teachers = CourseTeacher.objects.filter(course=course)
    return render(request, "mytutor/details.html", {"course": course, "teachers": course_teachers})


def findtutors(request):
    context_dict = {}
    teachers = User.objects.filter(role="teacher")
    context_dict["teachers"] = teachers
    return render(request, 'mytutor/find_tutors.html', context=context_dict)


def user_profile(request, id):
    user = User.objects.get(id=id)
    profile = user.profile
    return render(request, "mytutor/profile.html", {"profile": profile})


def signup(request):
    if request.user.is_authenticated:
        return redirect('/')
    form = UserRegistrationForm(request.POST or None)
    context = {'form': form}
    if form.is_valid():
        user = form.save(commit=False)
        user.save()
        messages.success(request, "You have successfully registered")
        return redirect('mytutor:index')
    return render(request, 'mytutor/signup.html', context=context)


def login_tutor(request):
    if request.user.is_authenticated:
        return redirect('/')
    form = UserLoginForm(request.POST or None)
    context = {'form': form}
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            try:
                p = Profile.objects.get(user_id=user.id)
            except Profile.DoesNotExist:
                Profile.objects.create(user=user)
            login(request, user)
            return redirect('/mytutor/dashboard')
        else:
            messages.warning(request, "Email or password is not correct. Please check again")
    return render(request, 'mytutor/login_tutor.html', context=context)


def login_student(request):
    if request.user.is_authenticated:
        return redirect('/')
    form = UserLoginForm(request.POST or None)
    context = {'form': form}
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('/mytutor/dashboard')
        else:
            messages.warning(request, "Email or password is not correct. Please check again")
    return render(request, 'mytutor/login_student.html', context=context)


@login_required(login_url="/")
def signout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('/')


@login_required(login_url="/")
def dashboard(request):
    user = request.user
    if user.role == "student":
        teacher_ids = Booking.objects.filter(student_id=user.id, is_accepted=True).values_list("teacher_id", flat=True)
        teachers = User.objects.filter(id__in=teacher_ids)
        courses = EnrolledCourse.objects.filter(user_id=user.id)
        return render(request, "mytutor/dashboard_student.html", {"teachers": teachers, "courses": courses})
    else:
        student_ids = Booking.objects.filter(teacher_id=user.id).values_list("student_id", flat=True)
        students = User.objects.filter(id__in=student_ids)
        return render(request, "mytutor/dashboard_teacher.html",
                      {"courses": user.my_courses.all(), "students": students})


@login_required(login_url="/")
def make_book_request(request, id):
    user = request.user
    if user.role == "student":
        Booking.objects.create(teacher_id=id, student_id=user.id, date=request.POST.get('date'),
                               time=request.POST.get('time'))
        messages.success(request, "Successfully requested for bookings")
    else:
        messages.warning(request, "You don't have permission")

    return redirect("mytutor:user.profile", id=id)


@login_required(login_url="/")
def booking_request(request):
    user = request.user
    requests = None
    if user.role == "teacher":
        requests = Booking.objects.filter(is_accepted=False, teacher_id=request.user.id)
    else:
        messages.warning(request, "You don't have permission")
    return render(request, "tutors/requests.html", {"booking_requests": requests})


@login_required(login_url="/")
def accept_request(request, id):
    user = request.user
    if user.role == "teacher":
        booking = Booking.objects.get(id=id)
        booking.is_accepted = True
        booking.save()
        messages.success(request, "You have accepted the request")
    else:
        messages.warning(request, "You don't have permission")
    return redirect("mytutor:my.booking.request")


@login_required(login_url="/")
def add_course(request):
    user = request.user
    course_id = int(request.GET.get('course_id', 0) or 0)
    if course_id > 0:
        CourseTeacher.objects.create(teacher_id=user.id, course_id=course_id)
        messages.success(request, "Added to your course list")
        return redirect("mytutor:dashboard")
    my_courses = user.my_courses.values_list("course_id", flat=True)
    other_courses = Course.objects.exclude(id__in=my_courses)
    return render(request, "tutors/add_course.html", {"courses": other_courses})


@login_required(login_url="/")
def add_comment(request):
    course_id = request.POST.get('course_id')
    content = request.POST.get('content')
    Comment.objects.create(user_id=request.user.id, course_id=course_id, content=content)
    messages.success(request, "Comment added")
    return redirect("mytutor:course-details", id=course_id, permanent=True)


@login_required(login_url="/")
def enroll(request, id):
    EnrolledCourse.objects.create(user_id=request.user.id, course_id=id)
    messages.success(request, "Successfully enrolled")
    return redirect("mytutor:course-details", id=id, permanent=True)


@login_required(login_url="/")
def profile(request):
    user = request.user
    if user.role != "teacher":
        messages.warning(request, "You don't have permission to view this page")
        return redirect("/")

    return render(request, "tutors/profile.html", {"user": user})


@login_required(login_url="/")
def edit_profile(request):
    user = request.user
    if user.role != "teacher":
        messages.warning(request, "You don't have permission to view this page")
        return redirect("/")

    form = ProfileUpdateForm(request.POST or None, request.FILES or None, instance=user.profile)

    if request.method == 'POST':
        if request.POST.get('education') or request.FILES.get('image'):
            form.save()

            return redirect("mytutor:profile")

    return render(request, 'tutors/profile-edit.html', {'user': user, 'form': form})

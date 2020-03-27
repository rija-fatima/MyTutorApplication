from django.urls import path
from mytutor import views

app_name = 'mytutor'

# this file gives the ability to label urls
urlpatterns = [
    path('', views.index, name='index'),
    path('browsecourse/', views.browsecourse, name='browsecourse'),
    path('details/<int:id>', views.course_details, name='course-details'),
    path('findtutors/', views.findtutors, name='findtutors'),
    path('signup/', views.signup, name='signup'),
    path('logintutor/', views.login_tutor, name='login-teacher'),
    path('loginstudent/', views.login_student, name='login-student'),
    path('signout/', views.signout, name='signout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/<int:id>', views.user_profile, name='user.profile'),
    path('booking-request/<int:id>', views.make_book_request, name='booking.request'),
    path('my-booking-requests', views.booking_request, name='my.booking.request'),
    path('booking-request-accept/<int:id>', views.accept_request, name='booking.request.accept'),
    path('add-course', views.add_course, name='add.course'),
    path('add-comment', views.add_comment, name='add.comment'),
    path('enroll/<int:id>', views.enroll, name='enroll'),
    path('profile', views.profile, name='profile'),
    path('edit-profile', views.edit_profile, name='edit.profile'),
]

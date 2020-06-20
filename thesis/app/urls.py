from django.urls import path
from . import views


urlpatterns = [
	path('', views.home, name="home"),
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),  
	path('logout/', views.logoutUser, name="logout"),
    path('account/', views.accountSettings, name="account"),
    #### Forms ####
    path('add_student/', views.add_students, name="add_student"),
    path('add_course/', views.add_courses, name="add_course"),
    path('add_classroom/', views.add_classrooms, name="add_classroom"),
    path('add_schedule/', views.add_schedules, name="add_schedule"),
    path('add_section/', views.add_sections, name="add_section"),
    ################# AI ############3
    path('align/', views.align, name='align'),
    path('upload/', views.upload, name="upload")
]
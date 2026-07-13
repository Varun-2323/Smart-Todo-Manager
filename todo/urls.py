from django.urls import path
from . import views

urlpatterns = [
    path('', views.todo_page, name='home'),
    path('login/', views.Login_page, name='login'),
    path('register/', views.Register_page, name='register'),
    path('dashboard/', views.Dashboard_page, name='dashboard'),
    path('add-task/', views.Add_Task, name='add_task'),
    path('edit-task/<int:id>/', views.Edit_Task, name='edit_task'),
    path('delete-task/<int:id>/', views.Delete_Task, name='delete_task'),
    path('complete-task/<int:id>/', views.Complete_Task, name='complete_task'),
    path("logout/", views.Logout_page, name="logout"),
    path("edit-profile/", views.Edit_Profile, name="edit_profile"),
]
from django.urls import path
from .views import *
from . import views

urlpatterns = [
	path('',userlist,name="userlist"),
	path('users/create/', views.create_user, name='create_user'),
	path('user/<int:user_id>/update/', views.update_user, name='update_user'),
    path('user/<int:user_id>/delete/', views.delete_user, name='delete_user'),

]
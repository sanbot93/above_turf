from django.urls import path
from .views import index, login_view, register, logout_view, golf_courses

urlpatterns = [
    path('', index, name='index'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('golf_course/', golf_courses, name='golfcourse'),
    #path('delete/', delete, name='delete'),
    #path('edit/', edit, name='edit'),
]


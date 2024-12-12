from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_list, name='blog_list'),
    path('new/', views.create_post, name='create_post'),
    path('<int:post_id>/', views.post_view, name='post_view'),  # برای مشاهده پست
    path('<int:post_id>/edit/', views.edit_post, name='edit_post'),  # برای ویرایش پست
    path('<int:post_id>/delete/', views.delete_post, name='delete_post'),  # برای حذف پست
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
]

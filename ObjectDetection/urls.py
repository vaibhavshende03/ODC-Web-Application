from django.contrib import admin
from django.urls import path
from ODCapp import views

urlpatterns = [
    # path('admin/', admin.site.urls),

    # path('',views.loginPage,name='login'),
    # path('logout/', views.logout, name='logout'),
    # path('signup/',views.signupPage,name='signup'),
    # path('index/',views.indexPage,name='index'),
    # path('video_feed/', views.video_feed, name='video_feed'),
    # path('get_detected_objects/', views.get_detected_objects, name='get_detected_objects'),
    

        path('admin/', admin.site.urls),
    path('', views.loginPage, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signupPage, name='signup'),
    path('index/', views.indexPage, name='index'),
    path('video_feed/', views.video_feed, name='video_feed'),
    path('get_detected_objects/', views.get_detected_objects, name='get_detected_objects'),
    path('leave_index_page/', views.leave_index_page, name='leave_index_page'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
]
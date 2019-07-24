from django.urls import path

from . import views


urlpatterns = [
    path('api/register/', views.RegisterView.as_view()),
    path('api/login/', views.LoginView.as_view()),
    path('api/logout/', views.LogoutView.as_view()),
    path('api/account/', views.AccountView.as_view()),
    path('api/account/verify/', views.AccountVerificationView.as_view(), name='account-verification'),

    path('api/lecturer/', views.LecturerListView.as_view()),
    path('api/lecturer/<int:pk>/', views.LecturerDetailView.as_view(), name='lecturer-detail'),

    path('api/lesson/', views.LessonListView.as_view()),
    path('api/lesson/<int:pk>/', views.LessonDetailView.as_view(), name='lesson-detail'),

    path('api/course/', views.CourseListView.as_view()),
    path('api/course/<int:pk>/', views.CourseDetailView.as_view(), name='course-detail'),

    path('api/course/<int:pk>/register/', views.RegisterOnCourseView.as_view(), name='register-on-course'),
    path('api/course/<int:pk>/unregister/', views.UnRegisterOnCourseView.as_view(), name='un-register-on-course'),
]

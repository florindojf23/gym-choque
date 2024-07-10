from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *
from . import views
from django.conf.urls.static import static
from .views import MyPasswordChangeView, MyPasswordChangeDoneView

urlpatterns=[
	path('', portal_view, name='portal'),
    path('home',home ,name='home'),
	path('member',member, name='member'),
	path('create_member', createMember, name='create_member'),
	path('update_member/<str:id>', updateMember, name='update_member'),
	path('delete_member/<str:pk>', deleteMember, name='delete_member'),
	path('detail_member/<str:pk>', detailMember,  name = 'detail_member'),
	path('csv_member/', csv_member, name="csv_member"),
	path('pdf_member/', pdf_member, name="pdf_member"),
	path('upload_csv/', upload_csv, name='upload_csv'),
    path('upload_success/', upload_success, name='upload_success'),

    path('gymclass',gymclass, name='gymclass'),
	path('create_gym_class', createGymClass, name='create_gym_class'),
	path('update_gym_class/<str:id>', updateGymClass, name='update_gym_class'),
	path('delete_gym_class/<str:pk>', deleteGymClass, name='delete_gym_class'),
	path('detail_gymclass/<str:pk>', detailGymClass,  name = 'detail_gymclass'),
	path('csv_gymclass/', csv_gymclass, name="csv_gymclass"),
	path('pdf_gymclass/', pdf_gymclass, name="pdf_gymclass"),

	path('enrollment',enrollment, name='enrollment'),
	path('create_enrollment', createEnrollment, name='create_enrollment'),
	path('update_enrollment/<str:id>', updateEnrollment, name='update_enrollment'),
	path('delete_enrollment/<str:pk>', deleteEnrollment, name='delete_enrollment'),
	path('detail_enrollment/<str:pk>', detailEnrollment,  name = 'detail_enrollment'),
	path('csv_enroll/', csv_enroll, name="csv_enroll"),
	path('pdf_enroll/', pdf_enroll, name="pdf_enroll"),

	path('schedule/today/', views.todays_schedule, name='todays_schedule'),
    path('schedule/week/', views.weekly_schedule, name='weekly_schedule'),
	path('reports/members/', views.member_report, name='member_report'),
    path('reports/classes/', views.class_report, name='class_report'),
    path('reports/enrollments/', views.enrollment_report, name='enrollment_report'),
	path('charts/', charts, name="charts"),
	path('chart_seksu_member/', chart_seksu_member, name="chart_seksu_member"),
	path('chart_municipiu/', chart_municipiu, name="chart_municipiu"),

	path('profile/<str:username>/', profile_view, name='profile'),
]
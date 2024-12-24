from django.urls import path

from works.views import JobApplicationCreateView


app_name = 'works'

urlpatterns = [
    path('job_application/', JobApplicationCreateView.as_view(), name='job_application'),
]
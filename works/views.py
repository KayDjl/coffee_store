from datetime import date
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from .forms import JobApplicationForm
from .models import JobApplication

class JobApplicationCreateView(FormView):
    template_name = 'works/job_application.html'
    form_class = JobApplicationForm
    success_url = reverse_lazy('main:index')

    def form_valid(self, form):
        data = form.cleaned_data
        JobApplication.objects.create(
            user=self.request.user if self.request.user.is_authenticated else None,
            full_name=data['full_name'],
            gender=data['gender'],
            phone=data['phone'],
            is_student=data['is_student'],
            position=data['position'],
            birth_date=data['birth_date'],
            residence=data['residence'],
            email=data['email'],
            marital_status=data['marital_status'],
            has_children=data['has_children'],
            work_experience=data['work_experience'],
            about_yourself=data['about_yourself'],
        )
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Заявка на работу"
        context['today_date'] = date.today().isoformat()  
        return context

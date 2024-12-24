from django.db import models

from users.models import User


class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'На рассмотрении'),
        ('approved', 'Одобрено'),
    ]

    GENDER_CHOICES = [
        ('male', 'Мужской'),
        ('female', 'Женский'),
    ]

    MARITAL_STATUS_CHOICES = [
        ('single', 'Не женат/Не замужем'),
        ('married', 'Женат/Замужем'),
        ('divorced', 'Разведен(а)'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='job_applications')
    full_name = models.CharField(max_length=255, verbose_name="ФИО")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name="Пол")
    phone = models.CharField(max_length=20, verbose_name="Номер телефона")
    is_student = models.BooleanField(verbose_name="Учишься")
    position = models.CharField(max_length=255, verbose_name="Должность")
    birth_date = models.DateField(verbose_name="Дата рождения")
    residence = models.CharField(max_length=255, verbose_name="Место проживания")
    email = models.EmailField(verbose_name="Email")
    marital_status = models.CharField(max_length=10, choices=MARITAL_STATUS_CHOICES, verbose_name="Семейное положение")
    has_children = models.BooleanField(verbose_name="Есть дети")
    work_experience = models.TextField(verbose_name="Опыт работы")
    about_yourself = models.TextField(verbose_name="Расскажите о себе")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name="Статус заявки")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата подачи заявки")

    def __str__(self):
        return f"Заявка от {self.full_name} ({self.status})"
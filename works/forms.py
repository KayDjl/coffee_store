from datetime import date
from django import forms

class JobApplicationForm(forms.Form):  
    GENDER_CHOICES = [
        ('male', 'Мужской'),
        ('female', 'Женский'),
    ]

    MARITAL_STATUS_CHOICES = [
        ('single', 'Не женат/Не замужем'),
        ('married', 'Женат/Замужем'),
        ('divorced', 'Разведен(а)'),
    ]

    full_name = forms.CharField()
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES)
    phone = forms.CharField()
    is_student = forms.ChoiceField(
        choices=[
            (True, 'Да'), 
            (False, 'Нет'),
            ],
    )
    position = forms.CharField()
    birth_date = forms.DateField()
    residence = forms.CharField()
    email = forms.EmailField()
    marital_status = forms.ChoiceField(
        choices=MARITAL_STATUS_CHOICES)
    has_children = forms.ChoiceField(
        choices=[
            (True, 'Да'), 
            (False, 'Нет'),
            ],
    )
    work_experience = forms.CharField()
    about_yourself = forms.CharField(required=False)

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        # Проверка, что дата не в будущем
        if birth_date > date.today():
            raise forms.ValidationError("Дата рождения не может быть в будущем.")

        # Проверка возраста (минимум 18 лет)
        today = date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        if age < 18:
            raise forms.ValidationError("Вам должно быть не менее 18 лет.")

        return birth_date  
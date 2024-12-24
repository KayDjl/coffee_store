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
    about_yourself = forms.CharField()
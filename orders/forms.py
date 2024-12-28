import re
from django import forms

class CreateOrderForm(forms.Form):
    
    phone_number = forms.CharField()
    requires_delivery = forms.ChoiceField(
        choices=[
            ("0", False),
            ("1", True),
            ],
        )
    delivery_address = forms.CharField(required=False)
    payment_on_get = forms.ChoiceField(
        choices=[
            ("0", "Оплата по карте"),
            ("1", "Наличными/картой при получении"),
            ],
        )
    
    def clean(self):
        cleaned_data = super().clean()
        requires_delivery = cleaned_data.get('requires_delivery')
        delivery_address = cleaned_data.get('delivery_address')
        
        if requires_delivery == '1' and not delivery_address:
            self.add_error('delivery_address', 'Адрес доставки обязателен при выборе доставки.')
        return cleaned_data
    


    def clean_phone_number(self):
        data = self.cleaned_data['phone_number']

        if not data.isdigit():
            raise forms.ValidationError("Номер телефона должен содержать только цифры")
        
        pattern = re.compile(r'^\d{11}$')
        if not pattern.match(data):
            raise forms.ValidationError("Неверный формат номера")
        
        return data

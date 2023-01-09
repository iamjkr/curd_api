from django import forms
from app.models import Product


class ProductForm(forms.ModelForm):
    #built in validations
    no = forms.IntegerField(min_value=101)
    class Meta:
        model = Product
        fields = '__all__'
    #with custom validationss
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price >= 500:
            return price
        else:
            raise forms.ValidationError('price must be greater than 500')
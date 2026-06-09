from django import forms
from .models import Order
class AddToCartForm(forms.Form):
    variant_id=forms.IntegerField(widget=forms.HiddenInput)
    quantity=forms.IntegerField(min_value=1, initial=1)
class CheckoutForm(forms.ModelForm):
    class Meta:
        model=Order
        fields=['full_name','email','phone','address','city','postcode']
        widgets={'address':forms.Textarea(attrs={'rows':3})}

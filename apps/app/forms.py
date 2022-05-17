from django import forms
# from django.forms import ModelChoiceField
from django.contrib.auth.models import User
from .models import Customer, Sites, Routers


class CustomerAddForm(forms.ModelForm):
	class Meta:
		model = Customer
		fields = ["cust_name","cust_status"]

class SiteAddForm(forms.ModelForm):
    select_customer = forms.ModelChoiceField(queryset=Customer.objects.all())
    class Meta:
        model = Sites
        fields = ["site_name","site_status","select_customer"]

class RouterAddForm(forms.ModelForm):
    class Meta:
        model = Routers
        fields = ["router_name","router_status","select_site","access_id","access_pwd","access_url","brand","firmware"]

class RouterOverviewForm(forms.ModelForm):
    class Meta:
        model = Routers
        fields = ["select_site","router_name","access_url","access_id","access_pwd"]

class RevealPasswordForm(forms.ModelForm):
    class Meta:
        model = Routers
        fields = ["router_name"]
   
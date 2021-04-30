from django import forms
from .models import FeeRequest
from .models import ACTIVITY_CHOICES, AGENCY_CHOICES

BOOTSTRAP_FORM_CONTROL_CLASS = 'form-control'
BOOTSTRAP_FORM_SELECT_CLASS = 'form-select'


class FeeRequestForm(forms.ModelForm):

    class Meta:
        model = FeeRequest
        exclude = ('level1', 'level2', 'agency', 'axe_analyse', 'timestamp', 'validated', 'user', 'refused', 'en_attente', 'observation_admin')

        widgets = {
            'activity': forms.Select(attrs={'class': BOOTSTRAP_FORM_SELECT_CLASS}, choices=ACTIVITY_CHOICES),
            'driver': forms.Select(attrs={'class': BOOTSTRAP_FORM_SELECT_CLASS}),
            'agency': forms.Select(attrs={'class': BOOTSTRAP_FORM_SELECT_CLASS}, choices=AGENCY_CHOICES),
            'date': forms.DateInput(attrs={'class': BOOTSTRAP_FORM_CONTROL_CLASS, 'type': 'date'}),
            'commentaire': forms.Textarea(attrs={'class': BOOTSTRAP_FORM_CONTROL_CLASS, 'rows': '3'}),
            
        }


class FeeValidateForm(forms.ModelForm):
    class Meta:
        model = FeeRequest
        exclude = ('level1', 'level2', 'timestamp', 'a_rembourser', 'user', 'en_attente', 'driver', 'date', 'commentaire', 'activity', 'code_vehicule', 'code_remorque', 'imat_vehicule', 'imat_remorque')
        widgets = {
            
            'axe_analyse': forms.Select(attrs={'class': BOOTSTRAP_FORM_SELECT_CLASS}),
            'agency': forms.Select(attrs={'class': BOOTSTRAP_FORM_SELECT_CLASS}, choices=AGENCY_CHOICES),
            'observation_admin': forms.Textarea(attrs={'class': BOOTSTRAP_FORM_CONTROL_CLASS, 'rows': '3'}),
            
        }


class FeeValidateForm2(forms.ModelForm):
    class Meta:
        model = FeeRequest
        exclude = ('level1', 'level2', 'timestamp', 'user', 'en_attente', 'commentaire', 'axe_analyse')
        widgets = {
            
            'driver': forms.Select(attrs={'class': BOOTSTRAP_FORM_SELECT_CLASS}),
            
            'observation_admin': forms.Textarea(attrs={'class': BOOTSTRAP_FORM_CONTROL_CLASS, 'rows': '3'}),
            
        }
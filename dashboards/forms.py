# Django
from django import forms

# Models
from dashboards.models import Lead
from django.contrib.auth.models import Group

class LeadForm(forms.ModelForm):
    # Model form del Lead
    class Meta:
        # Configuración del Form
        model = Lead
        fields = ("etapa",)

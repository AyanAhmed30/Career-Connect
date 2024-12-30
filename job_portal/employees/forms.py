from django import forms
from .models import AppliedJob

class AppliedJobForm(forms.ModelForm):
    class Meta:
        model = AppliedJob
        fields = ['resume']  # You can add more fields like 'job' if required

    resume = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
from django import forms

class MessageForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Type your message here...'}))

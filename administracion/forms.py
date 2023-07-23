from django import forms

class EmailForm(forms.Form):
    asunto = forms.CharField()
    mensaje = forms.CharField(widget=forms.Textarea)

from django import forms

class EmailForm(forms.Form):
    """
    Form class for sending emails.

    This form is used to create a basic email form with fields for the email subject and message. It provides two fields:
    'asunto' for the subject of the email (as a CharField) and 'mensaje' for the message of the email (as a CharField with
    a Textarea widget to allow multiline text input).

    Note:
        It's important to validate the data submitted through this form before sending emails to prevent any potential
        security issues.

    Attributes:
        asunto (CharField): The subject of the email.
        mensaje (CharField with Textarea widget): The message content of the email.
    """
    asunto = forms.CharField()
    mensaje = forms.CharField(widget=forms.Textarea)

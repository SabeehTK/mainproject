from django import forms
from listing.models  import Property
from listing.models import Enquiry

class AddPropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = "__all__"

class EnquiryForm(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = ['phone_number','email','message']

class EnquiryAcceptedForm(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = ['visiting_date','agent_response']
        widgets = {
            'visiting_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'agent_response': forms.Textarea(attrs={'rows': 3}),
        }

class EnquiryRejectedForm(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = ['agent_response']
        widgets = {
            'agent_response': forms.Textarea(attrs={'rows': 3}),
        }

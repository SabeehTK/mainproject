from django import forms
from listing.models  import Property

class AddPropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = "__all__"
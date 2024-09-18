from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import Car


def clean_license_number(self):
    license_number = self.cleaned_data["license_number"]
    if len(license_number) != 8:
        raise ValidationError("License number must be 8 characters long")
    if (
            license_number[:3] != license_number[:3].upper()
            or not license_number[:3].isalpha()
    ):
        raise ValidationError("First 3 characters must be uppercase chars")
    try:
        int(license_number[3:])
    except ValueError:
        raise ValidationError("last 5 characters must be a numbers")
    return license_number


class DriverCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "email"
        )


class DriverLicenseUpdateForm(forms.ModelForm):

    class Meta:
        model = get_user_model()
        fields = ("license_number",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = ["manufacturer", "model", "drivers"]

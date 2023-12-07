from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from . import models

#for admin
class AdminSigupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username already exists.")
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        errors = []

        # Custom validation logic
        if len(password) < 8:
            errors.append("Password must be at least 8 characters long.")

        if not any(char.isdigit() for char in password):
            errors.append("Password must contain at least one digit.")

        if not any(char.isalpha() for char in password):
            errors.append("Password must contain at least one letter.")


        if errors:
            raise forms.ValidationError(errors)

        return password


#for student related form
class StudentUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("")
        return username
    def clean_password(self):
        password = self.cleaned_data.get('password', '')  # Set a default value if password is None
        try:
            validate_password(password, self.instance)
        except ValidationError as e:
            raise forms.ValidationError(str(e))
        return password

    def clean(self):
        cleaned_data = super().clean()
        self.clean_password()  # Call the clean_password method explicitly
        return cleaned_data


class StudentExtraForm(forms.ModelForm):
    class Meta:
        model=models.StudentExtra
        fields=['roll','cl','mobile','fee','status']

    def clean_roll(self):
        roll = self.cleaned_data.get('roll')
        if models.StudentExtra.objects.filter(roll=roll).exists():
            raise forms.ValidationError("Invalid roll number.")
        return roll

    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
        if models.StudentExtra.objects.filter(mobile=mobile).exists():
            raise forms.ValidationError("This contact number is already registered.")
        return mobile



#for teacher related form
class TeacherUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("")
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password', '')  # Set a default value if password is None
        try:
            validate_password(password, self.instance)
        except ValidationError as e:
            raise forms.ValidationError(str(e))
        return password

    def clean(self):
        cleaned_data = super().clean()
        self.clean_password()  # Call the clean_password method explicitly
        return cleaned_data
class TeacherExtraForm(forms.ModelForm):
    class Meta:
        model=models.TeacherExtra
        fields=['salary','mobile','status']

    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
        if models.StudentExtra.objects.filter(mobile=mobile).exists():
            raise forms.ValidationError("This contact number is already registered.")
        return mobile



#for Attendance related form
presence_choices=(('Present','Present'),('Absent','Absent'))
class AttendanceForm(forms.Form):
    present_status=forms.ChoiceField( choices=presence_choices)
    date=forms.DateField()

class AskDateForm(forms.Form):
    date=forms.DateField()




#for notice related form
class NoticeForm(forms.ModelForm):
    class Meta:
        model=models.Notice
        fields='__all__'



#for contact us page
class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))

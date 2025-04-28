from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from member.models import *
# from bootstrap_datepicker_plus import DatePickerInput



class DateInput(forms.DateInput):
    input_type = 'date'


class UserReigsterForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            # 'username',
            # 'password1',
            # 'password2',
            'first_name',
            'last_name',
            'email'
        ]


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'name_korean',
            'address',
            'phone_mobile',
            'phone_office',
        ]



class ProfileUpdateBirthdayForm(forms.Form):
    date_of_birth = forms.DateField(widget=DateInput)
    date_joined = forms.DateField(widget=DateInput)

class UserRegisterCodeForm(forms.Form):
    code = forms.CharField(label="코드입력")


class CareerUpdateForm(forms.ModelForm):
    class Meta:
        model = Career
        fields = [
            'career1_company',
            'career1_position',
            'career1_detail',
            'career1_start',
            'career1_end',
            'career2_company',
            'career2_position',
            'career2_detail',
            'career2_start',
            'career2_end',
            'career3_company',
            'career3_position',
            'career3_detail',
            'career3_start',
            'career3_end',
            'career4_company',
            'career4_position',
            'career4_detail',
            'career4_start',
            'career4_end',
            'career5_company',
            'career5_position',
            'career5_detail',
            'career5_start',
            'career5_end',

        ]
        widgets = {
            'career1_start': forms.DateInput(format='%Y-%m-%d', attrs={'placeholder': 'e.g.) 2020-03-04'}),
            'career1_end': forms.DateInput(format='%Y-%m-%d', attrs={'placeholder': 'e.g.) 2020-03-04'}),
            'career2_start': forms.DateInput(format='%Y-%m-%d', attrs={'placeholder': 'e.g.) 2020-03-04'}),
            'career2_end': forms.DateInput(format='%Y-%m-%d', attrs={'placeholder': 'e.g.) 2020-03-04'}),
            'career3_start': forms.DateInput(format='%Y-%m-%d', attrs={'placeholder': 'e.g.) 2020-03-04'}),
            'career3_end': forms.DateInput(format='%Y-%m-%d', attrs={'placeholder': 'e.g.) 2020-03-04'}),
            'career4_start': forms.DateInput(format='%Y-%m-%d', attrs={'placeholder': 'e.g.) 2020-03-04'}),
            'career4_end': forms.DateInput(format='%Y-%m-%d', attrs={'placeholder': 'e.g.) 2020-03-04'}),
            'career5_start': forms.DateInput(format='%Y-%m-%d', attrs={'placeholder': 'e.g.) 2020-03-04'}),
            'career5_end': forms.DateInput(format='%Y-%m-%d', attrs={'placeholder': 'e.g.) 2020-03-04'}),

        }


class EducationUpdateForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = [
            'education1_level',
            'education1_detail',
            'education1_end',
            'education2_level',
            'education2_field',
            'education2_detail',
            'education2_start',
            'education2_end',
            'education3_level',
            'education3_field',
            'education3_detail',
            'education3_start',
            'education3_end',
            'education4_level',
            'education4_field',
            'education4_detail',
            'education4_start',
            'education4_end',
            'education5_level',
            'education5_field',
            'education5_detail',
            'education5_start',
            'education5_end',

        ]
        widgets = {
            'education1_end': forms.DateInput(format='%Y-%m-%d', attrs={'placeholder': 'e.g.) 2020-03-04'}),
            'education2_start': forms.DateInput(format='%Y-%m-%d', attrs={'placeholder': 'e.g.) 2020-03-04'}),
            'education2_end': forms.DateInput(format='%Y-%m-%d', attrs={'placeholder': 'e.g.) 2020-03-04'}),
            'education3_start': forms.DateInput(format='%Y-%m-%d', attrs={'placeholder': 'e.g.) 2020-03-04'}),
            'education3_end': forms.DateInput(format='%Y-%m-%d', attrs={'placeholder': 'e.g.) 2020-03-04'}),
            'education4_start': forms.DateInput(format='%Y-%m-%d', attrs={'placeholder': 'e.g.) 2020-03-04'}),
            'education4_end': forms.DateInput(format='%Y-%m-%d', attrs={'placeholder': 'e.g.) 2020-03-04'}),
            'education5_start': forms.DateInput(format='%Y-%m-%d', attrs={'placeholder': 'e.g.) 2020-03-04'}),
            'education5_end': forms.DateInput(format='%Y-%m-%d', attrs={'placeholder': 'e.g.) 2020-03-04'}),



        }


# class WorkingTimeForm(forms.ModelForm):
#     class Meta:
#         model = Working_Time
#         fields = [
#             'wkt_start',
#             'wkt_end',
#         ]


class DateInput(forms.DateInput):
    input_type = 'date'


class VacationDateInputForm(forms.Form):
    start_date = forms.DateField(widget=DateInput)
    end_date = forms.DateField(widget=DateInput)


class HolidayDateInputForm(forms.Form):
    date_holiday = forms.DateField(widget=DateInput)


# class HolidayTimeInputForm(forms.Form):
#     time = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))


class ExampleForm(forms.Form):
    my_date_field = forms.DateField(widget=DateInput)





class TakeoverForm(forms.Form):
    takeover = forms.ModelChoiceField(queryset=Profile.objects.all())

    def __init__(self, *args, **kwargs):
        division_code = kwargs.pop('division_code', None)
        super(TakeoverForm, self).__init__(*args, **kwargs)

        if division_code:
            self.fields['takeover'].queryset = Profile.objects.filter(division_code=division_code)


class InformReferenceForm(forms.Form):
    inform_reference = forms.ModelMultipleChoiceField(
        queryset=Profile.objects.all(),  widget=forms.CheckboxSelectMultiple,)

    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company', None)
        super(InformReferenceForm, self).__init__(*args, **kwargs)

        if company:
            self.fields['inform_reference'].queryset = Profile.objects.filter(company=company).order_by('division_code')

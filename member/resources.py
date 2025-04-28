from import_export import resources
from member.models import *
from import_export.fields import Field
from django.contrib.auth.models import User


class UserResource(resources.ModelResource):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class MemberResource(resources.ModelResource):
    # date_created = Field(attribute='created', column_name='date_created22222')
    class Meta:
        model = Member  # no field == default == all fields
        # fields = []
        exclude = ['date_created', 'date_updated'] 


class TeamResource(resources.ModelResource):
    class Meta:
        model = Team  
        exclude = ['date_created', 'date_updated'] 


class Member2TeamResource(resources.ModelResource):
    class Meta:
        model = Member2Team  
        exclude = ['date_created', 'date_updated'] 


class DivisionResource(resources.ModelResource):
    class Meta:
        model = Division  
        exclude = ['date_created', 'date_updated'] 

        
class Team2DivisionResource(resources.ModelResource):
    class Meta:
        model = Team2Division 
        exclude = ['date_created', 'date_updated']  


class Member2DivisionResource(resources.ModelResource):
    class Meta:
        model = Member2Division 
        exclude = ['date_created', 'date_updated']  


class CompanyResource(resources.ModelResource):
    class Meta:
        model = Company  
        exclude = ['date_created', 'date_updated'] 

    
class Division2CompanyResource(resources.ModelResource):
    class Meta:
        model = Division2Company  
        exclude = ['date_created', 'date_updated'] 


class Member2CompanyResource(resources.ModelResource):
    class Meta:
        model = Member2Company  
        exclude = ['date_created', 'date_updated'] 


class GroupResource(resources.ModelResource):
    class Meta:
        model = Group  
        exclude = ['date_created', 'date_updated'] 


class Company2GroupResource(resources.ModelResource):
    class Meta:
        model = Company2Group  
        exclude = ['date_created', 'date_updated'] 





########################################################################


class ProfileResource(resources.ModelResource):
    class Meta:
        model = Profile 
        exclude = ['date_created', 'date_updated'] 
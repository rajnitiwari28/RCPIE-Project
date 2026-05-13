# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import AcademicCoordinator, CunsultancyProof, DeanResearch, EnterprenuerProof, InnovationProof, Patent, UserProfile, Faculty, RCConvener, DepartmentDRC, OtherDepartmentDRCHead

class UserCreationForm(UserCreationForm):
    ROLE_CHOICES = [
        ('Academic Coordinator', 'Academic Coordinator'),
        ('Research_Dean', 'Research_Dean'),
        ('DRC_Member', 'DRC_Member'),
        ('Faculty', 'Faculty'),
        ('RC Convener', 'RC Convener'),
        ('Department DRC', 'Department DRC'),
        ('Other Department DRC Head', 'Other Department DRC Head'),
        
    ]
    user_id = forms.CharField(max_length=10)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    mob = forms.CharField(max_length=15)
    email = forms.EmailField(required=True)
    department = forms.CharField(max_length=100)
    gender = forms.CharField(max_length=10)
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True)

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'user_id', 'email', 
            'mob', 'department', 'gender', 'role', 
            'username', 'password1', 'password2'
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
            user_profile = UserProfile.objects.create(
                user=user,
                mob=self.cleaned_data['mob'],
                department=self.cleaned_data['department'],
                gender=self.cleaned_data['gender'],
                role=self.cleaned_data['role'],
                is_approved=False  # Initially set to False

            )
            
            role = self.cleaned_data['role']
            if role == 'Faculty':
                 Faculty.objects.create(
                    user_profile=user_profile, 
                    first_name=user.first_name,
                    last_name=user.last_name,
                    mob=user_profile.mob,
                    email=user.email,
                    department=user_profile.department,
                    gender=user_profile.gender,
                )
            elif role == 'RC Convener':
                RCConvener.objects.create(user_profile=user_profile)
            elif role == 'Department DRC':
                DepartmentDRC.objects.create(user_profile=user_profile)
            elif role == 'Other Department DRC Head':
                OtherDepartmentDRCHead.objects.create(user_profile=user_profile)
            elif role == 'Academic Coordinator':
                AcademicCoordinator.objects.create(user_profile=user_profile)
            elif role == 'Research_Dean':
                DeanResearch.objects.create(user_profile=user_profile)
        return user


from django import forms
from .models import Patent

class PatentForm(forms.ModelForm):
    class Meta:
        model = Patent
        fields = '__all__' 

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        if not title:
            self.add_error('title', 'Title is required')
        return cleaned_data




from .models import PublishedPaper

from django import forms
from .models import PublishedPaper, Faculty  # your Faculty model

from .models import PublishedPaper, ResearchProposal
from django.contrib.auth.models import User

class PublishedPaperForm(forms.ModelForm):

    class Meta:
        model = PublishedPaper
        fields = [
            'title','rcid','cmrit_faculties','students_involved',
            'co_authors','journal_conference','journal_name',
            'accepted_date','presented_date','published_date','journal_type',
            'paper_type','isbn_doi','proof_link','remarks','published_site_link'
        ]
        widgets = {
            'title': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['title'].queryset = ResearchProposal.objects.filter(
                user_profile__user=user
            )
            

from django import forms
from .models import ProjectProposal

class ProjectCompletionForm(forms.ModelForm):
    class Meta:
        model = ProjectProposal
        fields = ['rc_id', 'proof_link']
        widgets = {
            'rc_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter RC ID'}),
            'proof_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter Google Drive link'}),
        }


from .models import ProposalProof

class ProposalProofForm(forms.ModelForm):
    class Meta:
        model = ProposalProof
        fields = ['proposal_title', 'proof_pdf_1', 'proof_pdf_2','proof_file']
class ConsultancyProofForm(forms.ModelForm):
    class Meta:
        model = CunsultancyProof
        exclude = ['faculty']
class EnterprenuerProofForm(forms.ModelForm):
    class Meta:
        model = EnterprenuerProof
        exclude = ['faculty']

class InnovationProofForm(forms.ModelForm):
    class Meta:
        model = InnovationProof
        exclude = ['faculty']
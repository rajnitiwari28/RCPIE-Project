from django.db import models

# Create your models here.
# models.py
from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    mob = models.CharField(max_length=15)
    email = models.EmailField()
    department = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    is_approved_by_admin = models.BooleanField(default=False)  # Approval field

    role = models.CharField(max_length=50, choices=[
        ('Research_Dean', 'Research_Dean'),
        ('DRC_Member', 'DRC_Member'),
        ('Academic Coordinator', 'Academic Coordinator'),
        ('Faculty', 'Faculty'),
        ('RC Convener', 'RC Convener'),
        ('Department DRC', 'Department DRC'),
        ('Other Department DRC Head', 'Other Department DRC Head')
    ])
    def __str__(self):
        return self.user.username
class Faculty(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE )
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    mob = models.CharField(max_length=15)
    email = models.EmailField()
    department = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)

   
from django.db import models
from django.utils.timezone import now

class ResearchProposal(models.Model):
    # User association
    user_profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    sent_to_department = models.CharField(max_length=100, null=True, blank=True)
    other_departments = models.ManyToManyField(UserProfile, blank=True, related_name="forwarded_proposals")

    # Proposal details
    title = models.CharField(max_length=255)
    corresponding_author = models.CharField(max_length=100)
    co_author = models.CharField(max_length=100)  # Changed to snake_case for consistency
    forum_for_submission = models.CharField(max_length=200)
    conference_or_journal_name = models.CharField(max_length=500)  # Changed to snake_case
    abstract = models.TextField()
    keywords = models.CharField(max_length=255)
    area = models.CharField(max_length=255)
    CMRIT_Citation = models.CharField(max_length=255)
    research_domain= models.CharField(max_length=255)
    RESEARCH_TYPE_CHOICES = [
        ("Mendatory Paper", "Mendatory Paper"),
        ("R load Paper", "R load Paper"),
    ]
    research_type = models.CharField(
        max_length=20,
        choices=RESEARCH_TYPE_CHOICES,
        default="Mendatory Paper"
    )
    # Files
    full_paper = models.FileField(upload_to='research_papers/', null=True, blank=True)
    plagiarism = models.FileField(upload_to='plagiarism_research_papers/', null=True, blank=True)

    # Status and Responses
    status = models.CharField(max_length=50, default='Pending')
    odeptstatus = models.CharField(max_length=50, default='Pending')

    rc_response = models.TextField(null=True, blank=True)
    rc_id = models.CharField(max_length=50, null=True, blank=True)
    dcr_comment = models.TextField(null=True, blank=True)
    drc_member_status = models.CharField(max_length=30, default='Pending')  # NEW
    drc_member_comments = models.TextField(blank=True, null=True) 
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set at creation
    updated_at = models.DateTimeField(auto_now=True)      # Automatically updated on save

    # Metadata or additional tracking
    is_plagiarism_checked = models.BooleanField(default=False)  # Tracks if plagiarism is verified
    is_approved_by_rc = models.BooleanField(default=False)      # Tracks RC approval
    is_sent_to_drc = models.BooleanField(default=False)         # Tracks if sent to DRC

    def __str__(self):
        return f"{self.title} - {self.status}"

    class Meta:
        ordering = ['-created_at']  # Default ordering by newest first
        verbose_name = "Research Proposal"
        verbose_name_plural = "Research Proposals"

# Notification model
from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
    NOTIFICATION_CHOICES = [
        ('research', 'Research'),
        ('patent', 'Patent'),
        ('project', 'Project'),
        ('enterprenuer', 'enterprenuer'),
        ('consultancy', 'consultancy'),
        ('innovation', 'innovation'),
        ('proposal', 'proposal'),
    ]

    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sent_notifications'
    )
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='received_notifications'
    )
    message = models.CharField(max_length=255)
    link = models.CharField(max_length=255, blank=True, null=True)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    notification_type = models.CharField(
        max_length=20, choices=NOTIFICATION_CHOICES, default='other'
    )

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.notification_type.title()} Notification to {self.receiver.username}: {self.message}"


    
# chat model

from django.db import models
from django.contrib.auth.models import User

class ChatMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']

    

#===========================================================================

class RCConvener(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    

class DepartmentDRC(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    email = models.EmailField(unique=False)  # Add email field
    mob = models.CharField(max_length=15, blank=True, null=True)  # Add mobile field
    department = models.CharField(max_length=100, blank=True, null=True)  # Add department field

from django.utils import timezone

class AcademicCoordinator(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    email = models.EmailField(unique=False)  # Add email field
    mob = models.CharField(max_length=15, blank=True, null=True)  # Add mobile field
    department = models.CharField(max_length=100, blank=True, null=True)  # Add department field
    uploaded_at = models.DateTimeField(default=timezone.now)
    excel_file = models.FileField(upload_to='uploads/excel_files/', blank=True, null=True)
    def __str__(self):
        return f"{self.user_profile} - {self.department}"


class DeanResearch(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    email = models.EmailField(unique=False)  # Add email field
    mob = models.CharField(max_length=15, blank=True, null=True)  # Add mobile field
    department = models.CharField(max_length=100, blank=True, null=True)  # Add department field
    uploaded_at = models.DateTimeField(default=timezone.now)
    excel_file = models.FileField(upload_to='uploads/excel_files/', blank=True, null=True)
    def __str__(self):
        return f"{self.user_profile} - {self.department}"

class DRC_Member(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    email = models.EmailField(unique=False)  # Add email field
    mob = models.CharField(max_length=15, blank=True, null=True)  # Add mobile field
    department = models.CharField(max_length=100, blank=True, null=True)  # Add department field
    uploaded_at = models.DateTimeField(default=timezone.now)
    excel_file = models.FileField(upload_to='uploads/excel_files/', blank=True, null=True)
    def __str__(self):
        return f"{self.user_profile} - {self.department}"

from django.utils import timezone

class DRCMemberReview(models.Model):
    research_proposal = models.ForeignKey('ResearchProposal', on_delete=models.CASCADE)
    drc_member = models.ForeignKey('DRC_Member', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),
        ('Reviewed', 'Reviewed'),
    ], default='Pending')
    comments = models.TextField(blank=True, null=True)
    reviewed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.drc_member.user_profile.user.username} - {self.research_proposal.id}"


class OtherDepartmentDRCHead(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    email = models.EmailField()
    mob = models.CharField(max_length=15, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.user_profile.user.username} ({self.department})"

    
class ProposalRouting(models.Model):
    proposal = models.ForeignKey(ResearchProposal, on_delete=models.CASCADE)
    drc = models.ForeignKey(OtherDepartmentDRCHead, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, default="Pending")
    comment = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('proposal', 'drc')  # Prevent duplicate entries


class Patent(models.Model):
    user_profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    sent_to_department = models.CharField(max_length=100, null=True, blank=True)

    # Existing fields
    title = models.CharField(max_length=255)
    abstract = models.TextField()
    keywords = models.TextField()
    corresponding_author = models.CharField(max_length=100)  # Applicant Name
    co_author = models.CharField(max_length=100)  # Inventor's Name
    related_work = models.TextField()  # Field of Invention
    full_pdf = models.FileField(upload_to='patent/')
    status = models.CharField(max_length=50, default='Pending')
    dcr_comment = models.TextField(blank=True, null=True)
    rc_id = models.CharField(max_length=50, null=True, blank=True)
    # **Newly Added Fields**
    address = models.TextField()  # Address for communication
    email_id = models.EmailField()  # Email ID
    prior_art = models.TextField(blank=True, null=True)  # Prior Art
    novelty = models.TextField(blank=True, null=True)  # Novelty compared to Prior Art
    submission_date = models.DateTimeField(null=True, blank=True)  # Allow NULL values 
    assigned_to_research_dean = models.BooleanField(default=False)
    dean_comment = models.TextField(null=True, blank=True)
    proof_link = models.URLField(max_length=500, blank=True, null=True) 

    PATENT_TYPE_CHOICES = [
        ("Mandatory Patent", "Mandatory Patent"),
        ("I load Patent", "I load Patent"),
    ]
    patent_type = models.CharField(
        max_length=20,
        choices=PATENT_TYPE_CHOICES,
        default="Mandatory Patent"
    )   
    def __str__(self):
        return self.title
    
class Patent_proof(models.Model):
    user_profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    rc_id = models.CharField(max_length=50, null=True, blank=True)
    title = models.CharField(max_length=255)
    abstract = models.TextField()
    patent_number = models.CharField(max_length=100, unique=True)
    proof_link = models.URLField(max_length=500, blank=True, null=True) 
    submitted_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title
class ProjectProposal(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    abstract = models.TextField()
    keywords = models.TextField()
    corresponding_author = models.CharField(max_length=100)
    faculty_included = models.CharField(max_length=255)
    proposal_form = models.FileField(upload_to='proposals/')
    plagiarism  = models.FileField(upload_to='Project/')
    status = models.CharField(max_length=50, default='Pending')
    dcr_comment = models.TextField(blank=True, null=True) 
    rc_id = models.CharField(max_length=50, null=True, blank=True)
    proof_link = models.URLField(max_length=500, blank=True, null=True) 

    def __str__(self):
        return self.title


class PublishedPaper(models.Model):
    faculty = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to faculty user
    title = models.ForeignKey(ResearchProposal, on_delete=models.CASCADE)
    rcid = models.CharField(max_length=50)
    cmrit_faculties = models.TextField()  # List of faculty involved
    students_involved = models.TextField()  # Names of students
    co_authors = models.TextField(blank=True, null=True)  # Co-authors outside CMRIT
    journal_conference = models.CharField(max_length=255)  # Journal/Conference
    journal_name = models.CharField(max_length=255)  # Name of Journal/Conference
    accepted_date = models.DateField()  # Accepted Month & Year
    presented_date = models.DateField(blank=True, null=True)  # Presented Month & Year
    published_date = models.DateField(blank=True, null=True)  # Published Month & Year
    journal_type = models.CharField(max_length=10, choices=[('Q1', 'Q1'), ('Q2', 'Q2'), ('Q3', 'Q3'), ('None', 'None')])
    paper_type = models.CharField(max_length=10, choices=[('Mendatory', 'Mendatory'), ('R_Load', 'R_Load')])

    isbn_doi = models.CharField(max_length=255, blank=True, null=True)  # ISBN/DOI/Volume/Issue/Page No
    proof_link = models.URLField()  # Proof Link
    remarks = models.TextField()  # Mandatory/ R Load/ Claimed Points
    published_site_link = models.URLField(blank=True, null=True)  # Published Site Link

    def __str__(self):
     return self.title.title

class ProposalProof(models.Model):
    faculty = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to faculty
    proposal_title = models.CharField(max_length=255)  # Proposal Title
    rc_id = models.CharField(max_length=50, blank=True, null=True)  # RC_ID (if available)
    proof_pdf_1 = models.FileField(upload_to='proposal_proofs/',blank=True, null=True)  # First PDF
    proof_pdf_2 = models.FileField(upload_to='proposal_proofs/',blank=True, null=True)  # Second PDF
    proof_file = models.FileField(upload_to='proposal_proofs/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Upload timestamp
    status = models.CharField(max_length=100, default='Pending')
    dcr_comment = models.TextField(blank=True, null=True)
    def __str__(self):
        return f"{self.faculty.username} - {self.proposal_title}"
class CunsultancyProof(models.Model):
    faculty = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to faculty
    cunsultancy_title = models.CharField(max_length=255)  # Proposal Title
    rc_id = models.CharField(max_length=50, blank=True, null=True)  # RC_ID (if available)
    proof_pdf_1 = models.FileField(upload_to='consultancy_document/',blank=True, null=True)  # First PDF
    proof_file = models.FileField(upload_to='consultancy_proofs/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Upload timestamp
    def __str__(self):
        return f"{self.faculty.username} - {self.cunsultancy_title}"
    
class EnterprenuerProof(models.Model):
    faculty = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to faculty
    enterprenuer_title = models.CharField(max_length=255)  # Proposal Title
    rc_id = models.CharField(max_length=50, blank=True, null=True)  # RC_ID (if available)
    proof_pdf_1 = models.FileField(upload_to='enterprenuer_document/',blank=True, null=True)  # First PDF
    proof_file = models.FileField(upload_to='enterprenuer_proofs/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Upload timestamp
    def __str__(self):
        return f"{self.faculty.username} - {self.enterprenuer_title}"
    
class InnovationProof(models.Model):
    faculty = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to faculty
    innovation_title = models.CharField(max_length=255) 
    rc_id = models.CharField(max_length=50, blank=True, null=True)  # RC_ID (if available)
    proof_pdf_1 = models.FileField(upload_to='innovation_proofs/')  # First PDF
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Upload timestamp
    def __str__(self):
        return f"{self.faculty.username} - {self.innovation_title}"
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import user_passes_test

# Import ALL views safely (NO name shadowing)
from RCPIEAPP import views


# ------------------- USER ROLE CHECKS -------------------
def is_rc_convener(user):
    return user.groups.filter(name='RC_Convener').exists()

def is_faculty(user):
    return user.groups.filter(name='Faculty').exists()

def is_department_drc(user):
    return user.groups.filter(name='Department_DRC').exists()

def is_other_department_drc_head(user):
    return user.groups.filter(name='Other_Department_DRC_Head').exists()


# ------------------- URL PATTERNS ------------------------
urlpatterns = [

    # -------- AUTHENTICATION -----------
    path('', LoginView.as_view(template_name='login.html'), name='login'),
    path('admin/', admin.site.urls),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('approval_pending/', views.approval_pending, name='approval_pending'),

    # -------- FACULTY -----------
    path('faculty/', user_passes_test(is_faculty)(views.faculty_home), name='faculty_home'),
    path('research_submission/', views.research_submission, name='research_submission'),
    path('notification/read/<int:notification_id>/', views.mark_notification_read, name='mark_notification_read'),

    # -------- ACADEMIC COORDINATOR --------
    path('academic_coordinator_home/', views.academic_coordinator_dashboard, name='Academic_Coordinator_home'),
    path('academic_coordinator/upload/', views.upload_excel, name='upload_excel'),
    path('academic_coordinator/delete_excel/', views.delete_excel, name='delete_excel'),
    path('academic_coordinator/download_excel/', views.download_excel_file, name='download_excel_file'),

    # -------- RC CONVENER --------
    path('rc_convener/', user_passes_test(is_rc_convener)(views.rc_convener_home), name='rc_convener_home'),
    path('view-all-research-proposals/', views.view_all_research_proposals, name='view_all_research_proposals'),
    path('load_proposals/', views.load_proposals, name='load_proposals'),
    path('view_proposal_details/', views.view_proposal_details, name='view_proposal_details'),
    path('update_proposal_status/', views.update_proposal_status, name='update_proposal_status'),
    path('send_to_dept_drc/', views.send_to_dept_drc, name='send_to_dept_drc'),

    # File Serving
    path('serve_pdf/<int:proposal_id>/', views.serve_pdf, name='serve_pdf'),
    path('serve-plagiarism/<int:proposal_id>/', views.serve_plagiarism, name='serve_plagiarism'),

    # RC ID
    path('generate_rc_id/', views.generate_rc_id, name='generate_rc_id'),
    path('update_rc_id/', views.update_rc_id, name='update_rc_id'),
    path('rc_id_generation/', views.rc_id_generation, name='rc_id_generation'),

    # -------- CHAT SYSTEM --------
    path('chat/<int:user_id>/', views.chat_view, name='chat_with_user'),
    path('get-messages/', views.get_messages, name='get_messages'),
    path('send_message/', views.send_message, name='send_message'),
    path('fetch_chat_messages/', views.fetch_chat_messages, name='fetch_chat_messages'),
    path('delete_all_messages/', views.delete_all_messages, name='delete_all_messages'),
    path('load_chat/', views.load_chat, name='load_chat'),
    path('send_chat_message/', views.send_chat_message, name='send_chat_message'),

    # -------- DEPARTMENT DRC --------
    path('dept_drc_home/', user_passes_test(is_department_drc)(views.dept_drc_home), name='dept_drc_home'),
    path('load_proposals_drc/', views.load_proposals_drc, name='load_proposals_drc'),
    path('load_patent_to_drc/', views.load_patent_to_drc, name='load_patent_to_drc'),

    path('update_proposal_status_drc/', views.update_proposal_status_drc, name='update_proposal_status_drc'),
    path('update_patent_status_drc/', views.update_patent_status_drc, name='update_patent_status_drc'),
    path('send_message_to_faculty/', views.send_message_to_faculty, name='send_message_to_faculty'),
    path('send_message_to_faculty_patent/', views.send_message_to_faculty_patent, name='send_message_to_faculty_patent'),
    path('load_proposal_p_drc/', views.load_proposal_p_drc, name='load_proposal_p_drc'),

    # -------- OTHER DEPARTMENT DRC --------
    path('other_dept_drc_home/', views.other_dept_drc_home, name='other_dept_drc_home'),
    path('load_proposals_odrc/', views.load_proposals_odrc, name='load_proposals_odrc'),
    path('get-other-dept-drcs/', views.get_other_dept_drcs, name='get_other_dept_drcs'),

    # ⭐ CORRECT URL (Your main issue solved here)
    path('send_to_other_dept_drc/', views.send_to_other_dept_drc, name='send_to_other_dept_drc'),

    path('update_proposal_status_odrc/', views.update_proposal_status_odrc, name='update_proposal_status_odrc'),

    # -------- PATENT --------
    path('patent_submission/', views.patent_submission, name='patent_submission'),
    path('load_patents/', views.load_patents, name='load_patents'),
    path('serve_pdf_patent/<int:patent_id>/', views.serve_pdf_patent, name='serve_pdf_patent'),
    path('upload_patent_proof/', views.upload_patent_proof, name='upload_patent_proof'),
    path('proof_details_patent/<str:rc_id>/', views.proof_details_patent, name='proof_details_patent'),
    path('load_patents_drc/', views.load_patents_drc, name='load_patents_drc'),

    # -------- PROPOSAL P --------
    path('upload-proposal-proof/', views.upload_proposal_proof, name='upload_proposal_proof'),
    path('load_proposal_p/', views.load_proposal_p, name='load_proposal_p'),
    path('serve_pdf_proposal_p/<int:proposal_p_id>/', views.serve_pdf_proposal_p, name='serve_pdf_proposal_p'),

    # -------- CONSULTANCY --------
    path('upload-consultancy-proof/', views.upload_consultancy_proof, name='upload_consultancy_proof'),
    path('load_consultancy/', views.load_consultancy, name='load_consultancy'),
    path('serve_pdf_consultancy/<int:consultancy_id>/', views.serve_pdf_consultancy, name='serve_pdf_consultancy'),

    # -------- ENTERPRENUER --------
    path('upload-enterprenuer-proof/', views.upload_enterprenuer_proof, name='upload_enterprenuer_proof'),
    path('load_enterprenuer/', views.load_enterprenuer, name='load_enterprenuer'),
    path('serve_pdf_enterprenuer/<int:enterprenuer_id>/', views.serve_pdf_enterprenuer, name='serve_pdf_enterprenuer'),

    # -------- INNOVATION --------
    path('upload-innovation-proof/', views.upload_innovation_proof, name='upload_innovation_proof'),
    path('load_innovation/', views.load_innovation, name='load_innovation'),
    path('serve_pdf_innovation/<int:innovation_id>/', views.serve_pdf_innovation, name='serve_pdf_innovation'),

    # -------- PROJECT --------
    path('project_submission/', views.project_submission, name='project_submission'),
    path('upload_project_proof/', views.upload_project_proof, name='upload_project_proof'),
    path('get_project_proof_link/<str:rc_id>/', views.get_project_proof_link, name='get_project_proof_link'),
    path('load_projects/', views.load_projects, name='load_projects'),
    path('serve_pdf_project/<int:project_id>/', views.serve_pdf_project, name='serve_pdf_project'),
    path('load_projects_drc/', views.load_projects_drc, name='load_projects_drc'),
    path('upload_research_proof/', views.upload_research_proof, name='upload_research_proof'),
    path('proof-details/<str:rc_id>/', views.proof_details, name='proof_details'),
    path("get-rc-id/", views.get_rc_id_research_proof, name="get_rc_id_research_proof"),

    # -------- EXPORT DATA --------
    path('export-excel/', views.export_proposals_to_excel, name='export_proposals_excel'),
    path('export-data/', views.export_all_data_excel, name='export_all_data_excel'),

    # -------- RESEARCH DEAN --------
    path('dean_research/', views.dean_research_dashboard, name='dean_research_dashboard'),
    path('DRC_Member/', views.DRC_Member_dashboard, name='DRC_Member_dashboard'),
    path('submit_drc_review/', views.submit_drc_review, name='submit_drc_review'),
    path('load_drc_members/', views.load_drc_members, name='load_drc_members'),
    path('send_to_drc_members/', views.send_to_drc_members, name='send_to_drc_members'),
    path('get_drc_members/', views.get_drc_members, name='get_drc_members'),
    path('send_to_drc_member/', views.send_to_drc_member, name='send_to_drc_member'),
    path('send_to_research_dean/', views.send_to_research_dean, name="send_to_research_dean"),
    path('load_research_dean_patents/', views.load_research_dean_patents, name="load_research_dean_patents"),
    path('update_research_dean_patent/', views.update_research_dean_patent, name="update_research_dean_patent"),
]

# Serve media files during debug
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

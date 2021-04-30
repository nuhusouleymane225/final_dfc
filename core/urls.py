from django.urls import path
from core import views


urlpatterns = [
    path('create-request/', views.FeeRequestCreateView.as_view(), name='create-fee-request'),
    path('', views.intro, name='intro'),
    path('home/', views.welcome_admin, name='home'),
    path('demandes/', views.demande_affiche, name='demandes'),
    path('demandes/traite/', views.demande_traffiche, name="dtraite"), #old
    path('admin2-demandes/', views.admin2_demande_affiche, name="demande-admin2"),
    path('admin-demandes/', views.admin_demande_affiche, name="demande-admin"),
    path('demande-treate/<int:id>', views.traitementDemande, name="demande-treate"),
    path('demande-treate2/<int:id>', views.traitementDemande2, name="demande-treate2"),
    path('fast-print/<int:id>', views.ImprimePdf, name="pdf_view"),
    path('reporting/', views.rapport_mensuel, name='report')
]

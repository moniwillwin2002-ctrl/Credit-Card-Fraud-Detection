from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.app_login, name="login"),
    path("logout/", views.app_logout, name="logout"),
    path("prediction/", views.prediction, name="prediction"),
    path("card-management/", views.card_management, name="card_management"),
    path("all-cards/", views.all, name="all"),
    path("apply-card/", views.apply_credit_card, name="apply_card"),
    path("application-status/", views.application_status, name="application_status"),
    path("approved-card/", views.approved_card, name="approved_card"),
    path("all-applications/", views.all_applications, name="all_applications"),
]

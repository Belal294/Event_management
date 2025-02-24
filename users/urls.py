from django.urls import path
from django.contrib.auth import views as auth_views
from users.views import sign_up, sign_in, sign_out, signup_view, admin_dashboard, assing_role, group_list,dashboard_redirect, admin_dashboard, organizer_dashboard, participant_dashboard, activate_user, CreateGroupView

urlpatterns = [
    path('sign-up/', sign_up, name='sign-up'), 
    path('login/', sign_in, name='login'),  
    path('logout/', sign_out, name='logout'),  

    path("auth-login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="auth-login"),
    path("auth-logout/", auth_views.LogoutView.as_view(), name="auth-logout"),
    path("signup/", signup_view, name="signup"),
    path('admin/dashboard/', admin_dashboard, name='admin-dashboard'),
    path('admin/<int:user_id>/assign-role/', assing_role, name='assign-role'),
    # path('admin/create-group/', create_group, name='create-group'),
    path("admin/create-group/", CreateGroupView.as_view(), name="create-group"),

    path('admin/group_list/', group_list, name='group_list'),
    path('dashboard/', dashboard_redirect, name='dashboard_redirect'),
    path('dashboard/organizer/', organizer_dashboard, name='organizer_dashboard'),
    path('dashboard/participant/', participant_dashboard, name='participant_dashboard'),
     path("activate/<int:user_id>/<str:token>/", activate_user, name="activate_user"),

]

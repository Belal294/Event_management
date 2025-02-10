# from django.urls import path
# from django.contrib.auth import views as auth_views
# from users.views import sign_up, sign_in, sign_out, signup_view

# urlpatterns = [
#     path('sign-up/', sign_up, name='sign-up'),
#     path('sign-in/', sign_in, name='sign-in'),
#     path('sign-out/', sign_out, name='logout'),
#     path('login/', sign_in, name='login'),
    
#     path("signup/", signup_view, name="signup"),
#     path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
#     path("logout/", auth_views.LogoutView.as_view(), name="logout"),

# ]



from django.urls import path
from django.contrib.auth import views as auth_views
from users.views import sign_up, sign_in, sign_out,signup_view

urlpatterns = [

    path('sign-up/', sign_up, name='sign-up'), 
    path('login/', sign_in, name='login'),  
    path('logout/', sign_out, name='logout'),  

    path("auth-login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="auth-login"),
    path("auth-logout/", auth_views.LogoutView.as_view(), name="auth-logout"),
    path("signup/", signup_view, name="signup"),
]

from django.urls import path

from accounts import views

app_name = "accounts"


urlpatterns = [
    # path("signup/", views.SignUpView.as_view(), name="signup"),
    path("signin/", views.SignInView.as_view(), name="signin"),
    path("signout/", views.signout, name="signout"),
    path('update_user/', views.update_user, name='update_user'),
    path('user/create/', views.user_create, name='user_create'),
    path('change-password/', views.PasswordChangeCustomView.as_view(), name='password_change'),
    path('change-password/done/', views.PasswordChangeCustomDoneView.as_view(), name='password_change_done'),
    path('users/', views.UserListView.as_view(), name='user-list'),
    path("users/<int:user_id>/details/", views.user_details, name="user-detail"),
    path('reset-password/<int:user_id>/', views.reset_user_password, name='reset-user-password'),

]

"""hallframe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin, auth
from django.contrib.auth import views as auth_views
from django.urls import path
from halls import views
from django.conf.urls.static import static
from django.conf import settings
#from django.views.i18n import JavaScriptCatalog


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home, name='home'),
    path('#about',views.home,name='about'),

    path('dashboard',views.dashboard, name='dashboard'),
    path('edashboard',views.edashboard, name='edashboard'),

    # AUTH
    #path('signup', views.SignUp.as_view(), name="signup")
    path('signup',views.signup,name='signup'),
    path('signup/tutor',views.TutorSignUpView.as_view(), name='account_signup'),
    path('signup/employee',views.EmployeeSignUpView.as_view(),name='employee_signup'),
    path('login', auth_views.LoginView.as_view(), name="account_login"),
    path('logout', auth_views.LogoutView.as_view(), name="account_logout"),
     # Password reset links (ref: https://github.com/django/django/blob/master/django/contrib/auth/views.py)
    path('change-password/',auth_views.PasswordChangeView.as_view(template_name='commons/change-password.html',success_url = '/'),name='change_password'),

    # Forget Password
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='commons/password-reset/password_reset_form.html',
             subject_template_name='commons/password-reset/password_reset_subject.txt',
             email_template_name='commons/password-reset/password_reset_email.html',
             # success_url='/login/'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='commons/password-reset/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='commons/password-reset/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='commons/password-reset/password_reset_complete.html'
         ),
         name='password_reset_complete'),

    #Halls
    path('halloffame/create', views.CreateHall.as_view(),name='create_hall'),
    path('halloffame/',views.allcategories, name='allcategories'),
    path('halloffame/<int:pk>', views.DetailHall.as_view(),name='detail_hall'),
    path('halloffame/<int:pk>/update', views.UpdateHall.as_view(),name='update_hall'),
    path('halloffame/<int:pk>/delete', views.DeleteHall.as_view(),name='delete_hall'),
    #challenges
    path('halloffame/createchallenge/<int:pk>/', views.CreateChallenge.as_view(),name='create_challenge'),
    path('halloffame/challenges/',views.allchallenges, name='allchallenges'),

    path('halloffame/challenges/gg/<int:pk>/update', views.UpdateChallenge.as_view(),name='update_challenge'),
    path('halloffame/challenges/gg/<int:pk>/delete', views.DeleteChallenge.as_view(),name='delete_challenge'),
    path('halloffame/challenges/gg/<int:pk>', views.DetailChallenge.as_view(),name='detail_challenge'),
    #Collecting Challenges for a particular Category
    path('halloffame/<int:pk>/challenges', views.seechallenges, name='seechallenges'),
    #Collecting Files for a particular challenge{% url 'seefiles' challenge.id %}
    path('halloffame/challenges/gg/<int:pk>/files',views.seefiles, name='seefiles'),
    #Collecting Solutions for a particular request{% url 'seesolutions' request.id%}
    path('halloffame/challenges/gg/<int:pk>/solutions',views.seesolutions,name='seesolutions'),
    #Collecting Payments for a particular Payment
    path('halloffame/challenges/gg/<int:pk>/payments',views.seepayments,name='seepayments'),

    #files for challenge
    path('halloffame/addfile/<int:pk>',views.AddFile.as_view(), name = 'add_file'),
    path('halloffame/challenges/gg/files/',views.allfiles, name='allfiles'),
    path('halloffame/challenges/gg/files/<int:pk>',views.DetailFile.as_view(),name='detail_file'),
    path('halloffame/challenges/gg/files/<int:pk>/update',views.UpdateFile.as_view(),name='update_file'),
    path('halloffame/challenges/gg/files/<int:pk>/delete',views.DeleteFile.as_view(),name='delete_file'),
    #solutions for request
    path('halloffame/addsolution/<int:pk>',views.AddSolution.as_view(), name = 'add_solution'),
    path('halloffame/challenges/gg/solutions/',views.allsolutions, name='allsolutions'),
    path('halloffame/challenges/gg/solutions/<int:pk>',views.DetailSolution.as_view(),name='detail_solution'),
    path('halloffame/challenges/gg/solutions/<int:pk>/update',views.UpdateSolution.as_view(),name='update_solution'),
    path('halloffame/challenges/gg/solutions/<int:pk>/delete',views.DeleteSolution.as_view(),name='delete_solution'),

    #payments
    path('halloffame/addpayment/<int:pk>',views.AddPayment.as_view(), name = 'add_payment'),
    path('halloffame/challenges/gg/payments/',views.allpayments, name='allpayments'),
    path('halloffame/challenges/gg/payments/<int:pk>',views.DetailPayment.as_view(),name='detail_payment'),
    path('halloffame/challenges/gg/payments/<int:pk>/update',views.UpdatePayment.as_view(),name='update_payment'),
    path('halloffame/challenges/gg/payments/<int:pk>/delete',views.DeletePayment.as_view(),name='delete_payment'),
    #request
    path('halloffame/requestchallenge/<int:pk>',views.RequestChallenge.as_view(), name='request_challenge'),
    path('halloffame/challenges/gg/requests/',views.allrequests, name='allrequests'),
    path('halloffame/challenges/gg/requests/<int:pk>',views.DetailRequest.as_view(),name='detail_request'),
    path('halloffame/challenges/gg/requests/<int:pk>/update',views.UpdateRequest.as_view(),name='update_request'),
    path('halloffame/challenges/gg/requests/<int:pk>/delete',views.DeleteRequest.as_view(),name='delete_request'),
    path('halloffame/challenges/gg/requests/<int:pk>/complete', views.completerequest,name='complete_request'),
    path('halloffame/challenges/gg/requests/<int:pk>/confirm', views.confirmrequest,name='confirm_request'),
    path('halloffame/challenges/gg/requests/<int:pk>/reject', views.reject_confirmed_request,name='reject_confirmed_request'),
    path('halloffame/challenges/gg/requests/<int:pk>/submit', views.submit_request,name='submit_request'),
    path('halloffame/challenges/gg/requests/<int:pk>/submit/reject', views.reject_submitted_request,name='reject_submitted_request'),
    path('halloffame/challenges/gg/requests/<int:pk>/complete/reject',views.reject_completed_request,name='reject_completed_request'),
    path('halloffame/challenges/gg/requests/<int:pk>/payment/completed',views.paymentcompleted,name='payment_completed'),
    path('halloffame/challenges/gg/requests/<int:pk>/payment/completed/reject',views.reject_payment_completed,name='reject_payment_completed'),
    #path('jsi18n', JavaScriptCatalog.as_view(),name='js-catlog')
    #Solving Arena
    path('halloffame/projects',views.allprojects,name='allprojects'),
    path('halloffame/assignments',views.allassignments,name='allassignments'),
    path('halloffame/TimeBoundChallenges',views.allTimeBoundChallenges,name='allTimeBoundChallenges'),
    #profilepage
    #Seeing Tutor Profile
    path('halloffame/profilepage/<int:pk>/employee',views.see_profile,name='see_profile'),
    path('halloffame/profilepage/<int:pk>',views.detail_profile,name='profilepage'),
    path('halloffame/profilepage/<int:pk>/update',views.UpdateProfile.as_view(),name='update_profile'),
    path('halloffame/create_profile',views.CreateProfile.as_view(),name='create_profile'),

]
urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

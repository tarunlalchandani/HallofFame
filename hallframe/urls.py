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
    path('dashboard',views.dashboard, name='dashboard'),
    path('edashboard',views.edashboard, name='edashboard'),
    # AUTH
    path('signup', views.SignUp.as_view(), name="signup"),
    path('login', auth_views.LoginView.as_view(), name="login"),
    path('logout', auth_views.LogoutView.as_view(), name="logout"),
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

    path('halloffame/<int:cpk>/challenges/gg/<int:pk>', views.DetailChallenge.as_view(),name='detail_challenge'),
    #Collecting Challenges for a particular Category
    path('halloffame/<int:pk>/challenges', views.seechallenges, name='seechallenges'),
    #Collecting Files for a particular challenge{% url 'seefiles' challenge.id %}
    path('halloffame/challenges/gg/<int:pk>/files',views.seefiles, name='seefiles'),
    #files for challenge
    path('halloffame/addfile/<int:pk>',views.AddFile.as_view(), name = 'add_file'),
    path('halloffame/challenges/gg/files/',views.allfiles, name='allfiles'),
    path('halloffame/challenges/gg/files/<int:pk>',views.DetailFile.as_view(),name='detail_file'),
    path('halloffame/challenges/gg/files/<int:pk>/update',views.UpdateFile.as_view(),name='update_file'),
    path('halloffame/challenges/gg/files/<int:pk>/delete',views.DeleteFile.as_view(),name='delete_file'),

    #path('jsi18n', JavaScriptCatalog.as_view(),name='js-catlog')
]
urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

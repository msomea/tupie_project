from django.urls import path
from . import views

app_name = 'tupie_app'
urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('add_item/', views.add_item, name='add_item'),
    path('get_districts/', views.get_districts, name='get_districts'),
    path('get_wards/', views.get_wards, name='get_wards'),
    path('get_places/', views.get_places, name='get_places'),
]
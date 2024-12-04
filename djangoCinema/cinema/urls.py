from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views
from .views import (
    DynamicListView, DynamicDetailView,
    DynamicUpdateView, DynamicDeleteView, DynamicCreateView, home, create_ticket
)
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', home, name='home'),
    path('<str:model_name>/list/', DynamicListView.as_view(), name='list'),
    path('<str:model_name>/<int:pk>/detail/', DynamicDetailView.as_view(), name='detail'),
    path('<str:model_name>/create/', DynamicCreateView.as_view(), name='create'),
    path('<str:model_name>/<int:pk>/update/', DynamicUpdateView.as_view(), name='update'),
    path('<str:model_name>/<int:pk>/delete/', DynamicDeleteView.as_view(), name='delete'),

    path('create_ticket/', views.create_ticket, name='create_ticket'),

    path('login/', views.login_user, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('registration/', views.registration, name='registration'),


]
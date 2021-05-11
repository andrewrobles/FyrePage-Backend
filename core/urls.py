from django.urls import path
from .views import current_user, UserList, links

urlpatterns = [
    path('current_user/', current_user),
    path('users/', UserList.as_view()),
    path('links/', links)
]

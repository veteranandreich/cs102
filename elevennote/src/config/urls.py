from django.contrib import admin
from django.urls import path, include

from django.views.generic import RedirectView

urlpatterns = [
    # Handle the root url.
    path('', RedirectView.as_view(url='notes/'), name='index'),

    # Accounts app
    path('accounts/', include('accounts.urls', namespace='accounts')),

    # Notes app
    path('notes/', include('notes.urls', namespace='notes')),

    # Admin
    path('admin/', admin.site.urls),
]
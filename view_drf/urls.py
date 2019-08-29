from django.conf import settings
from django.urls import path, re_path, include, reverse_lazy
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import RedirectView

from .users.views import register, token, refresh_token, revoke_token, \
    UserList, UserDetails, CatList, CatDetails


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/users/', UserList.as_view()),
    path('api/v1/users/<slug:id>/', UserDetails.as_view()),
    path('api/v1/cats/', CatList.as_view()),
    path('api/v1/cats/<int:pk>/', CatDetails.as_view()),
    #authentication
    path('authentication/register/', register),
    path('authentication/token/', token),
    path('authentication/token/refresh/', refresh_token),
    path('authentication/token/revoke/', revoke_token),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),

    # the 'api-root' from django rest-frameworks default router
    # http://www.django-rest-framework.org/api-guide/routers/#defaultrouter
    re_path(r'^$', RedirectView.as_view(url=reverse_lazy('api-root'), permanent=False)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

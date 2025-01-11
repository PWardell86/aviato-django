from django.contrib import admin

from django.urls import path, include   

from core.views import StopView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/trip/', StopView.as_view()),
    path('api/', include('rest_framework.urls'))
]

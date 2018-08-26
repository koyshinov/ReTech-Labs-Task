from django.conf.urls import url, include
from rest_framework import routers
from core import views
from core.views import signin, signout
from django.views.decorators.csrf import csrf_exempt

router = routers.DefaultRouter()
router.register(r'tasks', views.TaskViewSet, base_name='tasks')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^signin$', csrf_exempt(signin), name="signin"),
    url(r'^signout$', signout, name="signout")]

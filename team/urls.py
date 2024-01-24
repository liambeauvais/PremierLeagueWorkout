from rest_framework import routers

from team.views import TeamViewset

router = routers.SimpleRouter()
router.register("", TeamViewset, basename="teams")

urlpatterns = [

]

urlpatterns += router.urls

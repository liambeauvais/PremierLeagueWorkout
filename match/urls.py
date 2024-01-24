from rest_framework import routers

from match.views import MatchViewset

router = routers.SimpleRouter()
router.register("", MatchViewset, basename="matchs")

urlpatterns = [

]

urlpatterns += router.urls

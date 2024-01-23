from rest_framework import routers

from team_championship_stats.views import TeamChampionshipStatsViewset

router = routers.SimpleRouter()
router.register("", TeamChampionshipStatsViewset, basename="championship_stats")

urlpatterns = [

]

urlpatterns += router.urls

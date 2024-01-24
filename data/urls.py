from rest_framework import routers

from data.views import DataViewset

router = routers.SimpleRouter()
router.register("", DataViewset, basename="Data")

urlpatterns = [

]

urlpatterns += router.urls

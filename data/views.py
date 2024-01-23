from django.http import HttpResponse
from rest_framework import viewsets, mixins
from rest_framework.decorators import action

from championship.models import Championship
from data.premier_league import transform_league_tables, transform_league_matches


class DataViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Championship.objects.all()
    serializer_class = None

    @action(detail=False, methods=['GET'])
    def premier_league_stats(self, request):
        return HttpResponse(transform_league_tables())

    @action(detail=False,methods=['GET'])
    def premier_league_matches(self, request):
        return HttpResponse(transform_league_matches())

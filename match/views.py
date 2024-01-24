from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, serializers

from match.models import Match


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = '__all__'


class MatchViewset(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer

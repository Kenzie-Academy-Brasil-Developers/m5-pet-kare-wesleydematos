from rest_framework import serializers
from .models import Sex
from groups.serializers import GroupSerializer
from traits.serializers import TraitSerializer

class PetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=50)
    age = serializers.IntegerField()
    weight = serializers.FloatField()
    sex = serializers.ChoiceField(
        choices = Sex.choices,
        default = Sex.DEFAULT,
    )
    group = GroupSerializer(read_only=True)
    traits = TraitSerializer(read_only=True, many=True)
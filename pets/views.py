from rest_framework.views import APIView, Request, Response
from .models import Pet
from .serializers import PetSerializer
from groups.models import Group
from traits.models import Trait
from rest_framework.pagination import PageNumberPagination


class PetView(APIView, PageNumberPagination):

    def get(self, request: Request) -> Response:
        all_pets = Pet.objects.all()

        result_page = self.paginate_queryset(all_pets, request)

        serializer = PetSerializer(result_page, many=True)

        return self.get_paginated_response(serializer.data)

    def post(self, request: Request) -> Response:
        serializer = PetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        group_list = serializer.validated_data.pop("group")
        traits_list = serializer.validated_data.pop("traits")
        pet_list = serializer.validated_data

        group_obj = Group.objects.filter(
                scientific_name__iexact=group_list["scientific_name"]
            ).first()

        if not group_obj:
            group_obj = Group.objects.create(**group_list)

        pet_obj = Pet.objects.create(**pet_list, group=group_obj)

        for trait in traits_list:
            trait_obj = Trait.objects.filter(
                name__iexact=trait["name"]
            ).first()

            if not trait_obj:
                trait_obj = Trait.objects.create(**trait)

            pet_obj.traits.add(trait_obj)

        serializer = PetSerializer(pet_obj)

        return Response(serializer.data, 201)

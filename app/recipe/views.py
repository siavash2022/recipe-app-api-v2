"""
views for recipe APIS

"""


from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from core.models import Recipe, Tag,Ingredient
from recipe import serializers
import user

from rest_framework import (
    viewsets,
    mixins,
    status
)


class RecipeViewSets(viewsets.ModelViewSet):
    """ view for mange recipe apis """

    serializer_class = serializers.RecipeDetailSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        return self.queryset.filter(user = self.request.user).order_by('-id')


    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.RecipeSerializers
        elif self.action == 'upload_image':
            return serializers.RecipeImageSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

    @action(methods=['POST'], detail = True, url_path = 'upload-image')
    def upload_image(self,request, pk=None):
        recipe = self.get_object()
        serializer = self.get_serializer(recipe, data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)

        return Response(serializer.errors,status= status.HTTP_400_BAD_REQUEST)



class TagViewSet(viewsets.ModelViewSet):
    """ view for mange Tag apis """

    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['get','head','put','patch','delete']



    def get_queryset(self):
        return self.queryset.filter(user = self.request.user).order_by('-id')


class IngredientViewSet(mixins.ListModelMixin,mixins.UpdateModelMixin, mixins.DestroyModelMixin , viewsets.GenericViewSet):

    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user = self.request.user).order_by('-id')
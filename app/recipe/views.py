from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response


from core.models import Tag, Ingredient, Recipe
from . import serializers


class BaseClassTagIngredients(viewsets.GenericViewSet,
                              mixins.ListModelMixin,
                              mixins.CreateModelMixin):
    

    authentication_classes=(TokenAuthentication,)
    permission_classes=(IsAuthenticated,)
    def get_queryset(self):
        # check for assigned only tag 
        assigned_only= bool(
            int(self.request.query_params.get('assigned_only', 0))
        )

        queryset = self.queryset
        if assigned_only:
            # distinct here to remove duplicate result 
            # only return unique tags/ ingredients
            queryset =  queryset.filter(recipe__isnull = False).distinct()
        
        return queryset.filter(
            user = self.request.user
        ).order_by('-name')

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

        

class TagViewSet(BaseClassTagIngredients):
   
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()

    
class IngredientViewSet(BaseClassTagIngredients):
    
    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all()


class RecipeViewSet(viewsets.ModelViewSet):
    """Manage recipes in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()
    

    def __intStr_to_int_list(self, str):
        return [int(str_id) for str_id in str.split(',')]


    def get_queryset(self):
        """ filtering query set if any params are passed to it """
        tags = self.request.query_params.get('tags')
        ingredients = self.request.query_params.get('ingredients')
        
        queryset = self.queryset
        if tags:
           
            tags_ids = self.__intStr_to_int_list(tags)
            queryset = queryset.filter(tags__id__in=tags_ids).distinct()
        if ingredients:
          
            ingredient_ids = self.__intStr_to_int_list(ingredients)
            queryset = queryset.filter(
                ingredients__id__in=ingredient_ids).distinct().distinct()


        return queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """ return the appropriate Serializer class for
            each action 
        """
        if self.action == 'retrieve':
            return serializers.RecipeDetailSerializer
        elif self.action == 'upload_image':
            return serializers.RecipeImageSerializer
        return self.serializer_class ## default
    
    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

    # create our custom upload image action
    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """ Upload image to a recipe """ 
        recipe = self.get_object()
        serializer = self.get_serializer(
            recipe,
            data = request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status = status.HTTP_200_OK
            )
        # error or invalid data
        return Response(
                serializer.errors,
                status = status.HTTP_400_BAD_REQUEST
        )

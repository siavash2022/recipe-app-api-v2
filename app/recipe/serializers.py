from dataclasses import fields
from pyexpat import model
from rest_framework import serializers
from core.models import Recipe,User,Tag,Ingredient,LikeRecipe,RecipeComment


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email','name']


class RecipeCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = RecipeComment
        fields = ['user','comment']


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ['name','id']
        read_only_fields = ['id']

class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ['name','id']
        read_only_fields = ['id']

class RecipeSerializers(serializers.ModelSerializer):

    user = UserSerializer( required = False )
    tags = TagSerializer( many = True , required = False )
    like_count = serializers.SerializerMethodField('get_likes_count')


    def get_likes_count(self, obj:Recipe) -> int:
        return LikeRecipe.objects.filter(recipe = obj).count()
    class Meta:
        model = Recipe
        fields = [
            'id', 'title', 'time_minutes', 'price', 'link','user','tags','like_count']
        read_only_fields = ['id']

    def _get_or_create_tags(self,tags,recipe):
        auth_user = self.context['request'].user
        for tag in tags:
            tag_obj , created = Tag.objects.get_or_create(
                user = auth_user,
                **tag
            )
            recipe.tags.add(tag_obj)

    def _get_or_create_ingredients(self, ingredients, recipe):
        """Handle getting or creating ingredients as needed."""
        auth_user = self.context['request'].user
        for ingredient in ingredients:
            ingredient_obj, created = Ingredient.objects.get_or_create(
                user=auth_user,
                **ingredient,
            )
            recipe.ingredients.add(ingredient_obj)

    def create(self, validated_data):
        tags = validated_data.pop('tags',[])
        ingredients = validated_data.pop('ingredients', [])
        recipe = Recipe.objects.create(**validated_data)
        self._get_or_create_tags(tags,recipe)
        self._get_or_create_ingredients(ingredients, recipe)

        return recipe

    def update(self, instance, validated_data):
        """Update recipe."""
        tags = validated_data.pop('tags', None)
        ingredients = validated_data.pop('ingredients', None)
        if tags is not None:
            instance.tags.clear()
            self._get_or_create_tags(tags, instance)
        if ingredients is not None:
            instance.ingredients.clear()
            self._get_or_create_ingredients(ingredients, instance)

        return super().update(instance , validated_data)

class RecipeDetailSerializer(RecipeSerializers):

    class Meta(RecipeSerializers.Meta):
        fields = RecipeSerializers.Meta.fields + ['descrip0tion','image']


class RecipeImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ["id","image"]
        read_only_fields = ['id']
        extra_kwargs = {'image':{'required':'True'}}

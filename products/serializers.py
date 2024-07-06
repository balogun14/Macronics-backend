from rest_framework import serializers

from products.models import Products, Category


class ProductCategoryReadSerializer(serializers.ModelSerializer):
    """
    Serializer class for product categories
    """

    class Meta:
        model = Category
        fields = "__all__"


class ProductReadSerializer(serializers.ModelSerializer):
    """
    Serializer class for reading products
    """

    seller = serializers.CharField(source="seller.get_full_name", read_only=True)
    category = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Products
        fields = "__all__"


class ProductWriteSerializer(serializers.ModelSerializer):
    """
    Serializer class for writing products
    """

    seller = serializers.HiddenField(default=serializers.CurrentUserDefault())
    category = ProductCategoryReadSerializer()

    class Meta:
        model = Products
        fields = (
            "id",
            "seller",
            "category",
            "name",
            "description",
            "image",
            "price",
            "quantity",
            "brand"
        )

    def create(self, validated_data):
        category = validated_data.pop("category")
        instance, created = Category.objects.get_or_create(**category)
        product = Products.objects.create(**validated_data, category=instance)

        return product

    def update(self, instance, validated_data):
        if "category" in validated_data:
            nested_serializer = self.fields["category"]
            nested_instance = instance.category
            nested_data = validated_data.pop("category")
            nested_serializer.update(nested_instance, nested_data)

        return super(ProductWriteSerializer, self).update(instance, validated_data)

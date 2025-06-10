from rest_framework import serializers
from .models import *

class amenity_serializer(serializers.ModelSerializer):
    class Meta:
        model = amenity
        fields = '__all__'

class room_amenity_serializer(serializers.ModelSerializer):
    class Meta:
        model = room_amenity
        fields = '__all__'

class room_type_serializer(serializers.ModelSerializer):
    class Meta:
        model = room_type
        fields = '__all__'


class coupon_serializer(serializers.ModelSerializer):
    class Meta:
        model = coupon
        fields = '__all__'


class service_category_serializer(serializers.ModelSerializer):
    class Meta:
        model = service_category
        fields = '__all__'


class food_menu_serializer(serializers.ModelSerializer):
    class Meta:
        model = food_menu
        fields = '__all__'


class service_subcategory_serializer(serializers.ModelSerializer):
    class Meta:
        model = service_subcategory
        fields = '__all__'


class service_serializer(serializers.ModelSerializer):

    category = service_category_serializer(read_only=True)
    subcategory = service_subcategory_serializer(read_only=True)

    class Meta:
        model = service
        fields = '__all__'


class symptom_serializer(serializers.ModelSerializer):
    class Meta:
        model = symptom
        fields = '__all__'


class customer_address_serializer(serializers.ModelSerializer):
    
    class Meta:
        model = customer_address
        fields = '__all__'
        read_only_fields = ['user']

    def create(self, validated_data):
        # Inject authenticated user manually
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    

    
class testimonials_serializer(serializers.ModelSerializer):
    class Meta:
        model = testimonials
        fields = '__all__'


class test_serializer(serializers.ModelSerializer):
    class Meta:
        model = test
        fields = '__all__'


class dog_breed_serializer(serializers.ModelSerializer):
    class Meta:
        model = dog_breed
        fields = '__all__'

class cat_breed_serializer(serializers.ModelSerializer):
    class Meta:
        model = cat_breed
        fields = '__all__'


class product_serializer(serializers.ModelSerializer):
    class Meta:
        model = product
        fields = '__all__'


class product_category_serializer(serializers.ModelSerializer):
    class Meta:
        model = product_category
        fields = '__all__'


class vaccination_serializer(serializers.ModelSerializer):
    class Meta:
        model = vaccination
        fields = '__all__'


class event_serializer(serializers.ModelSerializer):
    class Meta:
        model = event
        fields = '__all__'



class consultation_type_serializer(serializers.ModelSerializer):
    class Meta:
        model = consultation_type
        fields = '__all__'

class online_consultation_type_serializer(serializers.ModelSerializer):
    class Meta:
        model = online_consultation_type
        fields = '__all__'


# Step 1: Create a serializer
class HomeBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = home_banner
        fields = ['image'] 
    
    def get_image(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url
from rest_framework import serializers
from apps.users.models import User, Address


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('uid', 'email', 'first_name', 'last_name',
                'phone_number', 'is_active', 'full_name', 
                'city')


class UserAddressSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Address
        exclude = ['id']
        read_only_fields = ['user']

    def create(self, validated_data):
        request = self.context['request']
        user = request.user
        is_default = validated_data.get('is_default', False)

        if is_default and Address.objects.filter(user=user, is_default=True).exists():
            raise serializers.ValidationError("You can only have one default address.")

        validated_data['user'] = user
        address = Address.objects.create(**validated_data)
        return address
    
    def get_user(self, obj):
        return obj.user.full_name


class UserDetailsSerializer(serializers.ModelSerializer):
    addresses = UserAddressSerializer(many=True)
    class Meta:
        model = User
        fields = ('uid', 'email', 'first_name', 'last_name',
            'full_name', 'city', 'state', 'profile_photo', 
            'phone_number', 'addresses')

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.city = validated_data.get('city', instance.city)
        instance.state = validated_data.get('state', instance.state)

        instance.save()
        return instance

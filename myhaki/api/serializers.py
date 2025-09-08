# myhaki/api/serializers.py
from rest_framework import serializers
from lawyers.models import User, Lawyer, CPDPoint

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'email', 'role', 'first_name', 'last_name', 'phone_number', 'image', 'is_deleted']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

class LawyerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Lawyer
        fields = ['lawyer_id', 'user', 'practice_number', 'specialization', 'longitude', 'latitude', 'verified', 'created_at', 'updated_at']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer().create(user_data)
        lawyer = Lawyer.objects.create(user=user, **validated_data)
        return lawyer

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            user_serializer = UserSerializer(instance.user, data=user_data, partial=True)
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()
        return super().update(instance, validated_data)

class CPDPointSerializer(serializers.ModelSerializer):
    lawyer = LawyerSerializer(read_only=True)
    lawyer_id = serializers.PrimaryKeyRelatedField(queryset=Lawyer.objects.all(), source='lawyer', write_only=True)

    class Meta:
        model = CPDPoint
        fields = ['cpd_id', 'lawyer', 'lawyer_id', 'case', 'description', 'points_earned', 'created_at', 'updated_at']
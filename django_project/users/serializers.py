from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Card, Transaction

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data['username'],
                                        email=validated_data['email'],
                                        password=validated_data['password'])
        return user


class CardSerializer(serializers.ModelSerializer):
    raw_number = serializers.CharField(write_only=True, min_length=12, max_length=19)

    class Meta:
        model = Card
        fields = ('id', 'card_type', 'masked_number', 'last4', 'raw_number')
        read_only_fields = ('id', 'masked_number', 'last4')

    def create(self, validated_data):
        raw = validated_data.pop('raw_number')
        cleaned = ''.join(filter(str.isdigit, raw))
        if len(cleaned) < 12:
            raise serializers.ValidationError('Card number is too short')
        data = {
            'user': self.context['request'].user,
            'last4': cleaned[-4:],
            'card_type': validated_data.get('card_type', 'UNKNOWN'),
            'masked_number': '**** **** **** ' + cleaned[-4:]
        }
        return Card.objects.create(**data)


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('id', 'user', 'card', 'amount', 'status', 'created_at', 'updated_at')
        read_only_fields = ('id', 'user', 'status', 'created_at', 'updated_at')


class TransactionAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

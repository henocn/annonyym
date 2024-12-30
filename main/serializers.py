from rest_framework import serializers


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("Les mots de passe ne correspondent pas.")
        return data
    

from rest_framework import serializers

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    pseudo = serializers.CharField(write_only=False, required=False, allow_blank=True)
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Les mots de passe ne correspondent pas.")
        
        if not data['username'] or not data['password'] or not data['confirm_password']:
            raise serializers.ValidationError("Les champs username, password et confirm_password sont obligatoires.")
        
        return data

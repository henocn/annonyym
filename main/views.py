import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from main.serializers import ChangePasswordSerializer, RegisterSerializer
from .models import Profile, AnonymousMessage
from rest_framework.permissions import IsAuthenticated


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class SendMessageView(APIView):

    def post(self, request, link):
        try:
            profile = Profile.objects.get(unique_link=link)
        except Profile.DoesNotExist:
            return Response({'error': 'Invalid link'}, status=status.HTTP_404_NOT_FOUND)

        content = request.data.get('content')
        if not content:
            return Response({'error': 'Content is required'}, status=status.HTTP_400_BAD_REQUEST)

        ip_address = get_client_ip(request)

        AnonymousMessage.objects.create( profile=profile, content=content, ip_address=ip_address )

        return Response({'message': 'Message sent successfully'}, status=status.HTTP_201_CREATED)



class ReceivedMessagesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)

        messages = profile.messages.all().values('content', 'created_at', 'readden', 'ip_address').order_by('-created_at')
        return Response(list(messages), status=status.HTTP_200_OK)









#-------------------------------------------------------------------------------#
#                    Partie reservée à l'authentification                       #
#-------------------------------------------------------------------------------#

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash


class ObtainAuthTokenView(APIView):

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Remplisez les deux champs.'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        if user is None:
            return Response({'error': 'Informations incorrectes.'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        # Récupérer les informations supplémentaires du profil
        profile = Profile.objects.get(user=user)

        return Response({
            'id': user.id,
            'username': profile.user.username,
            'unique_link': profile.unique_link,
            'access_token': access_token,
            'refresh_token': str(refresh)
        }, status=status.HTTP_200_OK)





class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        
        if serializer.is_valid():
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']

            user = request.user
            if not user.check_password(old_password):
                return Response({'error': 'Ancien mot de passe incorrect'}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()

            update_session_auth_hash(request, user)
            return Response({'message': 'Mot de passe changé avec succès.'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class RegisterView(APIView):

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data['username']
            pseudo = serializer.validated_data['pseudo']
            password = serializer.validated_data['password']

            try:
                user = User.objects.create_user(username=username, password=password)
            except Exception:
                return Response({"error": "Nom d'utilisateur existe déjà. Choisissez un autre."}, status=status.HTTP_400_BAD_REQUEST)

            user.save()
            profile = Profile(user=user, pseudo=pseudo)
            profile.save()

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response({
                'id': user.id,
                'username': profile.user.username,
                'unique_link': profile.unique_link,
                'access_token': access_token,
                'refresh_token': str(refresh),
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

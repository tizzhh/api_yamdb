from random import randint

from django.core.exceptions import BadRequest
from django.core.mail import send_mail
from rest_framework import filters, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .permissions import IsAdmin
from api.serializers import (
    CustomTokenObtainPairSerializer,
    UserSerializerAdmin,
    UserSerializerAuth,
)
from custom_user.models import CustomUser


@api_view(['POST'])
def get_custom_token(request):
    serializer = CustomTokenObtainPairSerializer(data=request.data)
    if serializer.is_valid():
        print(serializer.validated_data)
        refresh = RefreshToken.for_user(serializer.validated_data['USER'])
        return Response(
            {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            status=status.HTTP_200_OK,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSetAuth(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializerAuth

    def create(self, request, *args, **kwargs):
        user = CustomUser.objects.filter(username=request.data.get('username'))
        serializer = self.get_serializer(data=request.data)
        if not user:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

        if user and user[0].email != request.data.get('email'):
            raise BadRequest('Incorrect email')

        confirmation_code = randint(10000, 99999)
        self.send_confirmation_code_email(request.data, confirmation_code)

        user = CustomUser.objects.get(username=request.data.get('username'))
        user.confirmation_code = confirmation_code
        user.save()

        headers = self.get_success_headers(serializer.initial_data)

        return Response(
            serializer.initial_data, status=status.HTTP_200_OK, headers=headers
        )

    def send_confirmation_code_email(self, data, confirmation_code):
        send_mail(
            subject='Confirmation code',
            message=f'Dear {data.get("username")}, here\'s your confirmation code: {confirmation_code}',
            from_email='yamdb@yamdb.net',
            recipient_list=(data.get('email'),),
            fail_silently=True,
        )


class UserViewSetAdmin(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializerAdmin
    permission_classes = (IsAdmin,)
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    pagination_class = PageNumberPagination

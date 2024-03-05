from random import randint

from django.core.exceptions import BadRequest
from django.core.mail import send_mail
from rest_framework import status, viewsets
from rest_framework.response import Response

from api.serializers import UserSerializerAuth, UserSerializerAdmin
from custom_user.models import CustomUser


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
        self.send_confirmation_code_email(request.data)

        headers = self.get_success_headers(serializer.initial_data)

        return Response(
            serializer.initial_data, status=status.HTTP_200_OK, headers=headers
        )

    def send_confirmation_code_email(self, data):
        send_mail(
            subject='Confirmation code',
            message=f'Dear {data.get("username")}, here\'s your confirmation code: {randint(10000, 99999)}',
            from_email='yamdb@yamdb.net',
            recipient_list=(data.get('email'),),
            fail_silently=True,
        )


class UserViewSetAdmin(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializerAdmin

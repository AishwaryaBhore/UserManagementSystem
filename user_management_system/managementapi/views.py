import os
from django.contrib.auth.models import User
from django.shortcuts import render
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import generics, status, request
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, RetrieveDestroyAPIView, \
    UpdateAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CustomUser
from .serializer import CustomSerializer, LoginSerializer, Generated_Token, CustomSerializerForUpdate, \
    ChangePasswordSerilizer
from .custompagination import MyPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import authenticate, login, logout


class UserList(ListAPIView):
    """"User List API is used for get the list of users"""
    queryset = CustomUser.objects.all()
    serializer_class = CustomSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterSet_fields = ['username', 'email', 'id']
    search_fields = ['first_name', 'last_name']
    pagination_class = MyPagination
    print(os.environ.get("EMAIL_USER"))

    def get_queryset(self):
        # If user is superuser then user can see
        # all database users and  if user is authenticated
        #  user then that user can see only his details
        if self.request.user.is_superuser:
            return CustomUser.objects.all()
        elif self.request.user.is_authenticated:
            return CustomUser.objects.filter(id=self.request.user.id)
        else:
            return CustomUser.objects.none()


class UserPost(CreateAPIView):
    """"User Create API is used to create users in API"""
    # When we are creating new user then activation
    # link will be sent on his mail while clicking on the
    # link his account will be activated
    queryset = CustomUser.objects.all()
    serializer_class = CustomSerializer

    def perform_create(self, serializer):
        variable = serializer.save()
        variable.set_password(variable.password)
        variable.save()


class UserUpdate(UpdateAPIView):
    """Used to Update the User"""
    queryset = CustomUser.objects.all()
    serializer_class = CustomSerializerForUpdate

    def get_queryset(self):
        if self.request.user.is_superuser:
            return CustomUser.objects.all()
        if self.request.user.is_authenticated:
            return CustomUser.objects.filter(id=self.request.user.id)
        else:
            return CustomUser.objects.none()


class UserDetailView(RetrieveDestroyAPIView):
    """"User Retrieve Update Delete API is used to Retrieve Update Delete users"""
    queryset = CustomUser.objects.all()
    serializer_class = CustomSerializer

    def get_queryset(self):
        # If user is then superuser can perform Retrieve Update and delete operation of all user
        if self.request.user.is_superuser:
            return CustomUser.objects.all()
        # If user is not superuser, but he is authenticated then he get his own details only
        if self.request.user.is_authenticated:
            return CustomUser.objects.filter(id=self.request.user.id)
        else:
            raise User.objects.none()


class LoginView(APIView):
    """" User Login API"""

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Retrieve the username and password from validated data
        try:
            user = authenticate(username=serializer.validated_data['username'],
                                password=serializer.validated_data['password'])
        except:
            Response({'message': 'This user does not exists'})

        if user:
            # send the request to make login
            login(request, user)
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'id': user.id})
        else:
            return Response({'error': 'Invalid details'}, status=400)


class LogoutView(APIView):
    """"User Logout API"""
    """"When we perform logout it will delete token"""

    def post(self, request):
        user = request.user
        if user.is_authenticated:
            token = Token.objects.filter(user=user)
            token.delete()
            logout(request)
            return Response({'message': 'Logged out'})
        else:
            return Response({'error': 'Please enter valid details'}, status=400)


class AccountActivation(APIView):

    def post(self, request):
        email = request.data.get('email')
        user = get_object_or_404(CustomUser, email=email)
        token = Generated_Token.make_token(user)
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        activate_url = f'http://127.0.0.1:8000/user/activation_link/{uidb64}/{token}/'
        return Response({'message': activate_url}, status=status.HTTP_200_OK)


@api_view(('GET',))
def activate(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except CustomUser.DoesNotExists:
        user = None
    if user is not None and Generated_Token.check_token(user, token):
        user.is_active = True
        user.save()
        return Response("acctivated successfully")
    else:
        return Response("Invalid link")


class ForgetPassword(APIView):
    """This class is used for foget password"""

    def post(self, request):
        email = request.data.get('email')
        user = get_object_or_404(CustomUser, email=email)
        token = Generated_Token.make_token(user)

        activate_url = f'http://127.0.0.1:8000/user/reset/{user.id}/{token}/'
        return Response({'message': activate_url}, status=status.HTTP_200_OK)


class ChangePassword(APIView):
    """This class change password"""

    def post(self, request, user_id, token):
        user = get_object_or_404(CustomUser, id=user_id)

        if not Generated_Token.check_token(user, token):
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CustomSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user.set_password(serializer.validated_data['new_password'])
        user.save()

        return Response({'message': 'password reset succesfully'}, status=status.HTTP_200_OK)

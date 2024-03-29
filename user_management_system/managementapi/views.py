from django.contrib.auth.models import User
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveDestroyAPIView, \
    UpdateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from . import serializer
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
    filterset_fields = ['username', 'email', 'id']
    search_fields = ['first_name', 'last_name']
    pagination_class = MyPagination

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
    permission_classes = ([IsAuthenticated])

    def get_queryset(self):
        if self.request.user.is_superuser:
            return CustomUser.objects.all()
        elif self.request.user == self.request.POST.get('user'):
            serializer.save(user=self.request.user)
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
        # If user is not superuser, but he is authenticated then he gets his own details only
        if self.request.user.is_authenticated:
            return CustomUser.objects.filter(id=self.request.user.id)
        else:
            return User.objects.none()


class LoginView(APIView):
    """" User Login API"""

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Retrieve the username and password from validated data
        user = serializer.validated_data['user']
        if user is not None:
            # send the request to make login
            login(request, user)
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'id': user.id})
        else:
            return Response({'error': 'Invalid details'}, status=400)


class LogoutView(APIView):
    """"User Logout API"""
    """"When we perform logout it will delete token"""

    def get(self, request):
        user = request.user
        if user.is_authenticated:
            token = Token.objects.filter(user=user)
            token.delete()
            logout(request)
            return Response({'message': 'Logged out'})
        else:
            return Response({'error': 'Please enter valid details'}, status=400)


class AccountActivation(APIView):
    """This class is used for user account activation
     when we execute AccountActivation API is will ask for
      email and by using email  it will generate token and uidb"""

    def post(self, request):
        email = request.data.get('email')
        user = get_object_or_404(CustomUser, email=email)
        token = Generated_Token.make_token(user)
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        activate_url = f'http://127.0.0.1:8000/user/activation_link/{uidb64}/{token}/'
        return Response({'message': activate_url}, status=status.HTTP_200_OK)


@api_view(('GET',))
def activate(request, uidb64, token):
    """This function is used for account activation in this
     function we will check user and token and make user.is_active=True"""

    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except CustomUser.DoesNotExists:
        user = None
    if user is not None and Generated_Token.check_token(user, token):
        user.is_active = True
        user.save()
        return Response("Your account acctivated successfully")
    else:
        return Response("Invalid link")


class ForgetPassword(APIView):
    """This class is used for forget password"""

    def post(self, request):
        email = request.data.get('email')
        user = get_object_or_404(CustomUser, email=email)
        token = Generated_Token.make_token(user)

        activate_url = f'http://127.0.0.1:8000/user/reset/{user.id}/{token}/'
        return Response({'message': activate_url}, status=status.HTTP_200_OK)


@api_view(('PUT',))
def changepassword(request, user_id, token):
    """This function used to change the password"""

    user = get_object_or_404(CustomUser, id=user_id)

    if not Generated_Token.check_token(user, token):
        return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = ChangePasswordSerilizer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user.set_password(serializer.validated_data['new_password'])
    user.save()

    return Response({'message': 'You have changed your password successfully'}, status=status.HTTP_200_OK)

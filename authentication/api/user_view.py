from rest_framework.generics import GenericAPIView
from authentication.models import User
from authentication.api import serializer
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password
from utils.response import res


class UserRegisterView(GenericAPIView):
    queryset = User
    serializer_class = serializer.UserRegistrationSerializer

    def post(self, request):
        user_data = request.data
        registration_credentials = self.serializer_class(data=user_data)

        if registration_credentials.is_valid():
            exist_user = User.objects.filter(
                username=registration_credentials.validated_data["username"]
            ).exists()

            if exist_user:
                return res(
                    message="The user already exists",
                    status=status.HTTP_400_BAD_REQUEST,
                )
            else:

                try:
                    registration_credentials.validated_data["password"] = make_password(
                        password=registration_credentials.validated_data["password"]
                    )
                    registration_credentials.save()
                    return res(
                        message="User Registered Sucessfully!",
                        data={},
                        status=status.HTTP_201_CREATED,
                    )
                except Exception as exec:
                    return res(
                        message="User Registration Failed!",
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        errors=str(exec),
                    )
        else:
            return res(
                message="User Registration Failed", status=status.HTTP_400_BAD_REQUEST
            )


class UserLoginView(GenericAPIView):
    serializer_class = serializer.LoginSerializer

    def post(self, request):
        login_data = request.data
        login_credential = self.serializer_class(data=login_data)
        if login_credential.is_valid():
            try:
                username = login_credential.validated_data["username"]
                password = login_credential.validated_data["password"]
                exists_user = User.objects.get(username=username)
                if not exists_user.check_password(password):
                    return res(
                        message="Invalid Credentials!",
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                else:
                    refresh = RefreshToken.for_user(exists_user)
                    return res(
                        message="Login Sucessful!",
                        status=status.HTTP_202_ACCEPTED,
                        data={
                            "access": str(refresh.access_token),
                            "refresh": str(refresh),
                        },
                    )
            except exists_user.DoesNotExist:
                return res(
                    message="User Does not Exist!", status=status.HTTP_404_NOT_FOUND
                )


class AllUsersView(GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = serializer.UserDetailsSerializer

    def get(self, request):
        try:
            all_users = User.objects.all()
            user_list = list(self.serializer_class(data=all_users, many=True).data)
            return res(
                message="Fetched all users!", data=user_list, status=status.HTTP_200_OK
            )
        except:
            return res(
                message="Failed to fetch users!",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

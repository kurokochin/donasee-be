from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings

from donasee.api.serializers.user import RegisterSerializer, UserSerializer, LoginSerializer

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class RegisterView(APIView):
    """
        Register

            Allowed Method: POST

            Headers: -
            Fields:
                username = user email (varchar)
                email = user email (varchar)
                password = user password (varchar)
                community_name = community name (varchar)
                admin_name = user name (varchar)


            Example:
                {
                    "email": "ricky@gmail.com",
                    "password": "asdasd123",
                    "community_name": "Gereja Bethel Indonesia",
                    "admin_name": "Ricky Putra Nursalim",
                    "docs_link": "https://docs.google.com/"
                }

            Response:
                Success:
                    Status Code: 200 (OK)
                    Response Data:
                        Fields:
                        - token : jwt token
                        - user : user data

                        Example:
                        {
                            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InJpY2t5QGdtYWlsLmNvbSIsInVzZXJfaWQiOjQsImVtYWlsIjoicmlja3lAZ21haWwuY29tIiwiZXhwIjoxNDk5NDgxNTczfQ.TFbJy3GR62JW54BLiI3aTTWYP9Cu2t_F6zbJQZMMkoQ",
                            "user": {
                                "id": 4,
                                "username": "ricky@gmail.com",
                                "email": "ricky@gmail.com",
                                "userprofile": {
                                    "id": 2,
                                    "community_name": "Gereja Bethel Indonesia",
                                    "admin_name": "Ricky Putra Nursalim",
                                    "status": "pending",
                                    "docs_link": "https://docs.google.com/",
                                    "error_message": null,
                                    "user": 4
                                }
                            }
                        }

                Error:
                    Status Code: 400 (Bad Request)
                    Response Data:
                        Example:
                        {
                            "detail": _error_message_
                        }
    """
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def post(self, request, format=None):
        ser = RegisterSerializer(data=request.data)
        if ser.is_valid():
            user = ser.save()
            ser_user = self.serializer_class(user)
            data = {
                "user": ser_user.data,
                "token": jwt_encode_handler(jwt_payload_handler(user))
            }
            return Response(data)
        return Response({'detail': ser.errors['non_field_errors'][0]}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
        Login

            Allowed Method: POST
            Headers: -
            Fields:
                email: user email (varchar)
                password: user password (varchar)

            Example:
                {
                    "email": "ricky@gmail.com",
                    "password": "ricky123"
                }

            Response:
                Success:
                    Status Code: 200 (OK)
                    Response Data:
                        Fields:
                        - token : jwt token
                        - user : user data

                        Example:
                            {
                                "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InJpY2t5QGdtYWlsLmNvbSIsInVzZXJfaWQiOjQsImVtYWlsIjoicmlja3lAZ21haWwuY29tIiwiZXhwIjoxNDk5NDgxOTgwfQ.PTytOjtL0liNXVz_-dzupUWj2vIs1Idkd6c9guicIKQ",
                                "user": {
                                    "id": 4,
                                    "username": "ricky@gmail.com",
                                    "email": "ricky@gmail.com",
                                    "userprofile": {
                                        "id": 2,
                                        "community_name": "Gereja Bethel Indonesia",
                                        "admin_name": "Ricky Putra Nursalim",
                                        "status": "pending",
                                        "docs_link": "https://docs.google.com/",
                                        "error_message": null,
                                        "user": 4
                                    }
                                }
                            }

                Error:
                    Status Code: 401 (Unauthorized)
                    Response Data:
                        Example:
                            {
                                "detail": "User not found"
                            }
    """

    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        ser = LoginSerializer(data=request.data)
        if ser.is_valid():
            try:
                user = User.objects.get(email=ser.validated_data)
            except User.DoesNotExist:
                return Response({"detail": 'User not found'}, status=status.HTTP_400_BAD_REQUEST)
            user_ser = UserSerializer(instance=user)
            data = {
                "user": user_ser.data,
                "token": jwt_encode_handler(jwt_payload_handler(user))
            }
            return Response(data)
        return Response({'detail': ser.errors['non_field_errors'][0]}, status=status.HTTP_401_UNAUTHORIZED)

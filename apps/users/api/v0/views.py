
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from .serializer import RegisterSerializer, LoginSerializer, UpdateUserSerializer, LogoutSerializer, UserSerializer
from ...models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema,OpenApiExample
from rest_framework.permissions import IsAuthenticated




class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    @extend_schema(
        request={
            "multipart/form-data": {
                "type": "object",
                "properties": {
                    "fullname": {"type": "string", "example": "Ibodullo Fayzullayev"},
                    "phone_number": {"type": "string", "example": "+998901234567"},
                    "email": {"type": "string", "example": "test@example.com"},
                    "password": {"type": "string", "example": "mySecret123"},
                    "confirm_password": {"type": "string", "example": "mySecret123"},
                },
                "required": ["fullname", "email", "password", "confirm_password"]
            }
        },
        responses={201: RegisterSerializer}
    )
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            # ✅ Tokenlar yaratish
            refresh = RefreshToken.for_user(user)
            access = str(refresh.access_token)

            return Response(
                {
                    "message": "Foydalanuvchi muvaffaqiyatli ro‘yxatdan o‘tdi!",
                    "access": access,
                    "refresh": str(refresh),
                },
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]
    @extend_schema(
        request={"multipart/form-data":
            {"type": "object",
                "properties": {
                    "email": {
                        "type": "string",
                        "description": "Tizimga kirish uchun emailingizni kiriitng",
                        "example": "example@gmail.com"
                    },
                    "password": {
                        "type": "string",
                        "description": "Tizimga kirish uchun passwordingizni kiriitng",
                        "example": ""
                    }


                },
            },
        },

        responses={
            200: {
                "type": "object",
                "properties": {
                    "refresh": {"type": "string"},
                    "access": {"type": "string"},
                    "message": {"type": "string"},
                }
            },
            401: {"description": "Email yoki parol noto‘g‘ri"}
        }
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Foydalanuvchini tekshirish
        user = authenticate(
            username=serializer.validated_data["email"],  # agar username email bo‘lsa
            password=serializer.validated_data["password"]
        )

        if user:
            # Token yaratish
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "message": "Login muvaffaqiyatli"
            }, status=status.HTTP_200_OK)

        return Response({"error": "Email yoki parol noto‘g‘ri"}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    @extend_schema(
        request=LogoutSerializer,
        responses={
            200: OpenApiExample(
                "Logout Success",
                value={"message": "Foydalanuvchi muvaffaqiyatli logout qilindi"}
            ),
            400: OpenApiExample(
                "Error",
                value={"error": "Token invalid yoki berilmagan"}
            )
        }
    )
    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            refresh_token = serializer.validated_data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {"message": "Foydalanuvchi muvaffaqiyatli logout qilindi"},
                status=status.HTTP_200_OK
            )

        except Exception:
            return Response(
                {"error": "Token invalid yoki berilmagan"},
                status=status.HTTP_400_BAD_REQUEST
            )
class UpdateProfileView(UpdateAPIView):
    serializer_class = UpdateUserSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    @extend_schema(
        request=UpdateUserSerializer,
        responses={200: UpdateUserSerializer}
    )
    def get_object(self):
        return self.request.user


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user  # tizimga kirgan foydalanuvchi
        serializer = UserSerializer(user)
        return Response(serializer.data)

profile = UserProfileView.as_view()
log_out = LogoutView.as_view()
login = LoginView.as_view()
register = RegisterView.as_view()
update_profile = UpdateProfileView.as_view()

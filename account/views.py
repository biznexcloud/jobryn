from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from jobrynbackend.permissions import IsEmailVerified
from drf_spectacular.utils import extend_schema
from .serializers import (
    RegisterSerializer, LoginSerializer, UserSerializer,
    VerifyOTPSerializer, ForgotPasswordSerializer, ResetPasswordSerializer
)


def get_tokens(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


class RegisterView(APIView):
    serializer_class = RegisterSerializer
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"msg": "Registered successfully"})


class LoginView(APIView):
    serializer_class = LoginSerializer
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            email=serializer.data['email'],
            password=serializer.data['password']
        )

        if not user:
            return Response({"msg": "Invalid credentials"}, status=400)

        if not user.is_email_verified:
            return Response({"msg": "Email not verified. Please verify your OTP."}, status=403)

        return Response({
            "token": get_tokens(user),
            "role": user.role
        })


class VerifyOTPView(APIView):
    serializer_class = VerifyOTPSerializer
    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')

        if not email or not otp:
            return Response({"msg": "Email and OTP are required"}, status=400)

        from .models import User
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"msg": "User not found"}, status=404)

        if user.is_email_verified:
            return Response({"msg": "Email is already verified"}, status=400)

        if user.otp != str(otp):
            return Response({"msg": "Invalid OTP"}, status=400)

        from django.utils import timezone
        if user.otp_expiry and timezone.now() > user.otp_expiry:
            return Response({"msg": "OTP has expired"}, status=400)

        # OTP is valid
        user.is_email_verified = True
        user.otp = None
        user.otp_expiry = None
        user.save()

        return Response({"msg": "Email verified successfully!"}, status=200)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated, IsEmailVerified]
    serializer_class = UserSerializer

    def get(self, request):
        return Response(UserSerializer(request.user).data)

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ForgotPasswordView(APIView):
    serializer_class = ForgotPasswordSerializer
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({"msg": "Email is required"}, status=400)

        from .models import User
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"msg": "User not found"}, status=404)

        import random
        from django.utils import timezone
        from datetime import timedelta
        from django.core.mail import send_mail

        otp = str(random.randint(100000, 999999))
        expiry = timezone.now() + timedelta(minutes=10)

        user.otp = otp
        user.otp_expiry = expiry
        user.save()

        # Send Email
        subject = "Password Reset OTP"
        message = f"Hi {user.name or 'User'},\n\nYour OTP for password reset is: {otp}\nThis OTP is valid for 10 minutes.\n\nBest regards,\nThe Jobryn Team"
        from django.conf import settings
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

        return Response({"msg": "OTP sent to your email"}, status=200)


class ResetPasswordView(APIView):
    serializer_class = ResetPasswordSerializer
    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')
        new_password = request.data.get('new_password')

        if not all([email, otp, new_password]):
            return Response({"msg": "Email, OTP, and new password are required"}, status=400)

        from .models import User
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"msg": "User not found"}, status=404)

        if user.otp != str(otp):
            return Response({"msg": "Invalid OTP"}, status=400)

        from django.utils import timezone
        if user.otp_expiry and timezone.now() > user.otp_expiry:
            return Response({"msg": "OTP has expired"}, status=400)

        # OTP is valid, reset password
        user.set_password(new_password)
        user.otp = None
        user.otp_expiry = None
        user.save()

        return Response({"msg": "Password reset successfully"}, status=200)
from django.shortcuts import render
from .models import User
from .serializer import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions, status
from threading import Thread
from message.SendOTP import sendotp
from django.utils import timezone
from datetime import timedelta


# Create your views here.
class UserAPIVIEW(APIView):
    def get(self, request, pk = None, format = None):
        id=pk
        if id is not None:
            user_data = User.object.get(id=id)
            serialized_user_data = UserDetailSerializer(user_data)
            return Response(serialized_user_data.data)
        user_data = User.object.all()
        serialized_user_data = UserDetailSerializer(user_data, many=True)
        return Response(serialized_user_data.data)

class UserSignupAPIVIEW(APIView):

    serializer_class = UserSignupSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        serialized_data = UserSignupSerializer(data=request.data)

        if serialized_data.is_valid():
            serialized_data.save()
            return Response({'msg':'Data Created'}, status=status.HTTP_201_CREATED)
        return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    serializer_class = LoginSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data['phone_number']
        user = User.object.get(phone_number=phone_number)
        msg_thread = Thread(target=sendotp,args=(user,))
        msg_thread.start()
        return Response({'info': 'successful! Otp sent', 'user_id': user.id, 'name': user.name}, status=status.HTTP_201_CREATED)


class ActivateView(APIView):
    serializer_class = OTPSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, user_id, *args, **kwargs):
        serialized_data = OTPSerializer(data= request.data)
        otp_code = request.data['otp']

        try:
            otp = OTP.objects.get(receiver=user_id)
        except(TypeError, OverflowError, ValueError, OTP.DoesNotExist):
            otp = None

        try:
            receiver = User.object.get(id=user_id)
        except(TypeError, OverflowError, ValueError, OTP.DoesNotExist):
            receiver = None

        if otp is None or receiver is None:
            raise ValidationError({'error': 'you are not a valid user'})

        elif timezone.now() - otp.sent_on >= timedelta(days=0, hours=0, minutes=1, seconds=0):
            # otp.delete()
            raise ValidationError({"Error": "OTP Expired"})
        if str(otp.otp)== str(otp_code):
            if receiver.active is False:
                serialized_data.is_valid(raise_exception=True)
                receiver.active = True
                receiver.save()
            otp.delete()
            #refresh, access = get_tokens_for_user(receiver)
            return Response({'message': 'Successful', 'refresh': "refresh", 'access': "access"})
        else:
            raise ValidationError({'error': 'Invalid OTP'})
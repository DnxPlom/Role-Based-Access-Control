from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.utils import IntegrityError

from accounts.models import UserModel
from accounts.permissions import AdminRole

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([AllowAny])
def login(request):
    username = request.data["username"]
    password = request.data["password"]

    user = authenticate(username=username, password=password)

    if user.is_superuser:
        model = UserModel.objects.get_or_create(user=user, role="admin")

    model = user.usermodel

    if model.first_login:
        model.first_login = False
        model.save()
        return Response({
            "username": user.username,
            "token": Token.objects.get_or_create(user=user)[0].key,
            "message": "Consider changing your first time login password"
        }, status=200)
    
    if user:
        return Response({
            "username": user.username,
            "token": Token.objects.get_or_create(user=user)[0].key
        }, status=200)
    return Response({ "message": "invalid details" }, status=401)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, AdminRole])
def add_user(request):
    try:
        username = request.data["username"]
        email = request.data["email"]
        password = request.data["password"]
        role = request.data["role"]
    except KeyError as e:
        return Response({ "message": "Provide all credentials" },
        status=400)

    if not request.user.is_superuser and role == "Admin":
        return Response({"Error": "You are not an administrator"}, status=401)

    try:
        user = User.objects.create(
            username=username,
            email=email
        )
        user.set_password(password)
        user.save()

        user_model = UserModel.objects.create(
            user=user,
            role=role
        )
        user_model.save()


    except IntegrityError as e:
        return Response({ "message": "User already exists" }, status=400)
    
    return Response({ "message": "Successful" }, status=200)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def users(request):
    
    role = request.GET.get("role")
    users = []

    if role not in ["admin", "staff", "basic"]:
        return Response({"message": "Incorrect user role"}, status=400)
    
    users = UserModel.objects.filter(role=role)
    users = [ {
        "username": user.user.username,
        "role": user.role
    } for user in users ]
    
    return Response({ "users": users }, status=200)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def change_password(request):
    try:
        password = request.data["password"]
    except KeyError as e:
        return Response({ "message": "Provide password" },
        status=400)
    
    user = request.user
    user.set_password(password)
    user.save()
    return Response({ "message": "Password Updated" },
        status=200)
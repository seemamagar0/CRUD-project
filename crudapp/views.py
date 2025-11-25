from django.shortcuts import get_object_or_404,render, redirect
from .models import Student
from .forms import RegistrationForm
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
# DRF imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import StudentSerializer
from .serializers import RegistrationSerializer
from django.contrib.auth.decorators import login_required

# Swagger imports
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password 
from django.contrib.auth import authenticate,login,logout
from django.core.exceptions import ValidationError

from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

# API: LIST + CREATE STUDENTS

# class StudentListCreate(APIView):
#     authentication_classes = [OAuth2Authentication]
#     permission_classes = [IsAuthenticated]

class UserRegistrationAPIView(APIView):

    @swagger_auto_schema(
        operation_description="Register a new user.",
        request_body=RegistrationSerializer,
        responses={
            201: openapi.Response(
                description="User registered successfully",
                schema=RegistrationSerializer
            ),
            400: "Invalid input data"
        }
    )
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            reg_user =serializer.save()
            try:
                send_mail(
                    subject='Registration Successful',
                    message=f'Hello {reg_user.first_name},\n\nThank you for registering!\n\nYour details have been saved successfully.',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[reg_user.email],  # adjust field name based on your model
                    fail_silently=False,
                )
            except Exception as e:
                # Log error but don't fail the registration
                print(f"Email failed: {e}")

            return Response(
                {"message": "User registered successfully", "data": serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(
            {"message": "Invalid input data", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

class StudentListCreate(APIView):

    # Swagger documentation for GET API
    @swagger_auto_schema(
        operation_description="Retrieve the list of all students.",
        responses={200: openapi.Response(description="Students retrieved successfully")}
    )
    def get(self, request):
        # Fetch all student records
        students = Student.objects.all()
        # Serialize many objects at once
        serializer = StudentSerializer(students, many=True)

        # Send API response
        return Response({
            "message": "Students retrieved successfully",
            "data": serializer.data
        })

    # Swagger documentation for POST API
    @swagger_auto_schema(
        operation_description="Create a new student record.",
        request_body=StudentSerializer,  # Accept serializer inputs in Swagger UI
        responses={
            201: openapi.Response(description="Student created successfully"),
            400: openapi.Response(description="Invalid input data"),
        }
    )
    def post(self, request):
        # Convert JSON → Python → validate
        serializer = StudentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()  # Insert new student into database
            return Response(
                {"message": "Student created successfully", "data": serializer.data},
                status=status.HTTP_201_CREATED
            )

        # Return validation errors
        return Response(
            {"message": "Invalid input data", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

# API: UPDATE STUDENT
class StudentUpdate(APIView):

    @swagger_auto_schema(
        operation_description="Update an existing student record.",
        request_body=StudentSerializer,
        responses={
            200: openapi.Response(description="Student updated successfully"),
            400: openapi.Response(description="Invalid input data"),
            404: openapi.Response(description="Student not found"),
        }
    )
    def put(self, request, id):

        # Check if student exists
        try:
            student = Student.objects.get(id=id)
        except Student.DoesNotExist:
            return Response(
                {"message": "Student not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Validate and update
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()  # Update existing student
            return Response(
                {"message": "Student updated successfully", "data": serializer.data}
            )

        # Validation errors
        return Response(
            {"message": "Invalid input data", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

# API: DELETE STUDENT
class StudentDelete(APIView):

    @swagger_auto_schema(
        operation_description="Delete a student record.",
        responses={
            200: openapi.Response(description="Student deleted successfully"),
            404: openapi.Response(description="Student not found"),
        }
    )
    def delete(self, request, id):

        # Try to find student
        try:
            student = Student.objects.get(id=id)
        except Student.DoesNotExist:
            return Response(
                {"message": "Student not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        student.delete()  # Delete record

        return Response(
            {"message": "Student deleted successfully"},
            status=status.HTTP_200_OK
        )

# FRONTEND VIEWS (HTML Templates)

# Home page – list all students
@login_required(login_url='log_in')
def home(request):
    data = Student.objects.all()
    return render(request, "crudappp/home.html", {"data": data})


# About page
@login_required(login_url='log_in')
def about(request):
    return render(request, "crudappp/about.html")

# Simple form for creating student (POST method)
@login_required(login_url='log_in')
def form(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid(): #valid the forms from the fields
            messages.success(request, "Your form is successfully submitted!")
            form.save() #save to the db
            return redirect('form')
    else:
        form = RegistrationForm() #initalize empty form for get request
    return render(request, 'crudappp/form.html', {'form': form})

@login_required(login_url='log_in')
def services(request):
    return render(request,'crudappp/services.html')

@login_required(login_url='log_in')
# Edit student record
def edit(request, id):
    student = get_object_or_404(Student, id=id)  # Get the student

    if request.method == "POST":
        form = RegistrationForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Student updated successfully!")
            return redirect("home")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegistrationForm(instance=student)  # pre-fill form with existing data

    return render(request, "crudappp/edit.html", {"form": form})


# Delete student – frontend delete
def delete(request, id):
    Student.objects.get(id=id).delete()
    return redirect("home")

def register(request):
    if request.method=="POST":
        data=request.POST
        first_name=data['first_name']
        last_name=data['last_name']
        username=data['username']
        email=data['email']
        password=data['password']
        confirm_password=data['confirm_password']

        if password == confirm_password:

            try: 
                validate_password(password)
                if User.objects.filter(username=username).exists():
                    messages.error(request, "Username already exist")
                    return redirect('register')
                if User.objects.filter(email=email).exists():
                    messages.error(request, "Email already exist")
                    return redirect('register')

                User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
                messages.success(request,"Successfully register")
                return redirect('register')
            except ValidationError as e:
                for error in e.messages:
                    messages.error(request,error)
                    return redirect('log_in')
        else:
            # print("error")
            messages.error(request,"Password and confirm password doesnot match")
            return redirect('register')

    return render(request,'auth/register.html')

def log_in(request):
    if request.method == "POST":
        username=request.POST['username']
        password=request.POST['password']
        remember_me=request.POST.get('remember_me')

        if not User.objects.filter(username=username).exists():
            messages.error(request, 'It is not registered.')
            return redirect('log_in')
        user=authenticate(username=username,password=password)

        if user is not None:
            login(request,user)
            if remember_me:
                request.session.set_expiry(3600000)
            else:
                request.session.set_expiry(0)
            return redirect('home')
        else:
            messages.error(request,"password is invalid")
        
    return render(request, 'auth/login.html')

def log_out(request):
    logout(request)
    return redirect('log_in')


class UserLoginAPIView(APIView):
    """
    Login API: returns JWT token
    """

    @swagger_auto_schema(
        operation_description="Login and obtain JWT token",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'password'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username of the user'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password of the user'),
            },
        ),
        responses={
            200: openapi.Response(
                description="JWT tokens returned",
                examples={
                    "application/json": {
                        "refresh": "refresh_token_here",
                        "access": "access_token_here",
                        "user": {
                            "id": 1,
                            "username": "testuser",
                            "email": "test@example.com",
                            "first_name": "John",
                            "last_name": "Doe"
                        }
                    }
                }
            ),
            400: "Invalid credentials"
        }
    )
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if not user:
            return Response({"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name
            }
        })
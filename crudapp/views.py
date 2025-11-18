from django.shortcuts import render, redirect
from .models import Student
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import StudentSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# API: LIST + CREATE 
class StudentListCreate(APIView):

    @swagger_auto_schema(
        operation_description="Retrieve the list of all students.",
        responses={
            200: openapi.Response(description="Students retrieved successfully"),
        }
    )
    def get(self, request):
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response({
            "message": "Students retrieved successfully",
            "data": serializer.data
        })

    @swagger_auto_schema(
        operation_description="Create a new student record.",
        request_body=StudentSerializer,
        responses={
            201: openapi.Response(description="Student created successfully"),
            400: openapi.Response(description="Invalid input data"),
        }
    )
    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Student created successfully", "data": serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(
            {"message": "Invalid input data", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )


# API: UPDATE
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
        try:
            student = Student.objects.get(id=id)
        except Student.DoesNotExist:
            return Response(
                {"message": "Student not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Student updated successfully", "data": serializer.data}
            )
        return Response(
            {"message": "Invalid input data", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )


#API: DELETE 
class StudentDelete(APIView):

    @swagger_auto_schema(
        operation_description="Delete a student record.",
        responses={
            200: openapi.Response(description="Student deleted successfully"),
            404: openapi.Response(description="Student not found"),
        }
    )
    def delete(self, request, id):
        try:
            student = Student.objects.get(id=id)
        except Student.DoesNotExist:
            return Response(
                {"message": "Student not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        student.delete()
        return Response(
            {"message": "Student deleted successfully"},
            status=status.HTTP_200_OK
        )


#FRONTEND VIEWS (WORKING)
def home(request):
    data = Student.objects.all()
    return render(request, "crudappp/home.html", {"data": data})


def about(request):
    return render(request, "crudappp/about.html")


def form(request):
    if request.method == "POST":
        Student.objects.create(
            name=request.POST['name'],
            email=request.POST['email'],
            address=request.POST['address'],
        )
        return redirect('home')

    return render(request, "crudapp/form.html")


def add(request):
    if request.method == "POST":
        Student.objects.create(
            name=request.POST['name'],
            email=request.POST['email'],
            address=request.POST['address']
        )
        return redirect("/")
    return render(request, "crudappp/add.html")


def edit(request, id):
    student = Student.objects.get(id=id)
    if request.method == "POST":
        student.name = request.POST['name']
        student.email = request.POST['email']
        student.address = request.POST['address']
        student.save()
        return redirect("home")
    return render(request, "crudappp/edit.html", {"student": student})


# FRONTEND DELETE (GET METHOD)
def delete(request, id):
    Student.objects.get(id=id).delete()
    return redirect("home")

from .forms import ChildForm
from django.shortcuts import render, redirect,get_object_or_404
from .models import Child, Documents
from rest_framework.views import APIView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from .serializers import ChildSerializer,DocumentsSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
# Create your views here.

class ChildListCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ChildSerializer

    def get(self, request):
        parent_id = request.user.id
        if parent_id:
            children = Child.objects.filter(parent_id=parent_id)
        else:
            children = Child.objects.none()

        serializer = ChildSerializer(children, many=True)
        return Response(serializer.data)

    class ChildCreateView(APIView):
        def post(self, request):

            # If the profile picture is coming as a file, you may want to handle it explicitly
            if 'profile_picture' in request.data:
                profile_picture = request.FILES.get('profile_picture')  # Use request.FILES for file uploads
                request.data['profile_picture'] = profile_picture

            serializer = ChildSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChildDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, child_id):
        return get_object_or_404(Child, pk=child_id)

    def get(self, request, child_id):
        child = self.get_object(child_id)
        serializer = ChildSerializer(child)
        return Response(serializer.data)

    def put(self, request, child_id):
        child = self.get_object(child_id)
        serializer = ChildSerializer(child, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, child_id):
        child = self.get_object(child_id)
        # Prepare data for the serializer
        data = request.data.copy()  # Create a mutable copy of request.data

        # Check if profile_picture is in the request and handle it
        if 'profile_picture' in request.FILES:
            data['profile_picture'] = request.FILES['profile_picture']  # Use request.FILES for file uploads
        print('data>>>>>', data)
        serializer = ChildSerializer(child, data=data, partial=True)
        print(data, '===========================')

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, child_id):
        child = self.get_object(child_id)
        child.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class DocumentsListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, child_id):
        documents = Documents.objects.filter(child_id=child_id)
        serializer = DocumentsSerializer(documents, many=True)
        return Response(serializer.data)
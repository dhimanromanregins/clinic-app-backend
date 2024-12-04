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
        print(parent_id, '================')

        # Check if parent_id exists
        if parent_id is not None:
            children = Child.objects.filter(parent=parent_id)
            print(children, '00000000000')
        else:
            children = Child.objects.none()

        # Serialize the data
        serializer = ChildSerializer(children, many=True)
        return Response(serializer.data)


class ChildCreateView(APIView):
    def post(self, request):
        print(request.data, '-------------------------------')

        # Ensure the parent field is set to the logged-in user (request.user)
        request.data['parent'] = request.user.id

        # Serialize the data
        serializer = ChildSerializer(data=request.data)

        # Check if the serializer data is valid
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # Log validation errors if serializer is invalid
        print('Validation errors:', serializer.errors)

        # Return the error responses
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
        data = request.data.copy()
        if 'profile_picture' in request.FILES:
            data['profile_picture'] = request.FILES['profile_picture']
        data = data.dict()
        serializer = ChildSerializer(child, data=data, partial=True)
        print('data>>>>>', data)
        print(data, '===========================')
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_200_OK)
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


class DocumentsByParentAndCategoryView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, category):
        parent_id = request.user.id
        documents = Documents.objects.filter(parent_id=parent_id, category=category)

        if not documents.exists():
            return Response({"message": "No documents found for the given parent and category."},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = DocumentsSerializer(documents, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DocumentsByChildAndCategoryView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, child_id, category):
        # Filter documents by child and category
        documents = Documents.objects.filter(child_id=child_id, category=category)

        if not documents.exists():
            return Response({"message": "No documents found for the given child and category."},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = DocumentsSerializer(documents, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from django.shortcuts import get_object_or_404
from .models import Leaves, CustomUser, SickLeaveRecords,ParentSickLeaveHistory
from .serializers import LeavesSerializer,SickLeaveRequestSerializer,ToWhomItMayConcernSerializer,ParentSickLeaveHistorySerializer, SickLeaveRecordsSerializer,ParentSickLeaveSerializer
from rest_framework.permissions import IsAuthenticated
from children.models import Child

class LeavesAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def get(self, request,):
        user = get_object_or_404(CustomUser, id=request.user.id)
        leaves = Leaves.objects.filter(user=user)
        serializer = LeavesSerializer(leaves, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        print(request.data)

        data = request.data.copy()
        try:
            data['start_date'] = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
            data['end_date'] = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
            data["user"] = request.user.id
        except ValueError as e:
            return Response({"error": f"Date format error: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = LeavesSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SickLeaveRequestAPIView(APIView):
    def post(self, request):
        serializer = SickLeaveRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SickLeaveRecordsByChildView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        child_id = self.request.query_params.get('child_id')
        if not child_id:
            return Response({"error": "child_id query parameter is required."}, status=400)

        try:
            # Ensure the child exists
            child = Child.objects.get(id=child_id)
        except Child.DoesNotExist:
            return Response({"error": "Child not found."}, status=404)

        # Get all sick leave records for this child
        sick_leave_records = SickLeaveRecords.objects.filter(children=child)
        serializer = SickLeaveRecordsSerializer(sick_leave_records, many=True)
        return Response(serializer.data)


class ParentSickLeaveCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        print(request.data, '--------')
        serializer = ParentSickLeaveSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ParentSickLeaveHistoryList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Get the list of parent sick leave history.
        """
        sick_leave_history = ParentSickLeaveHistory.objects.filter(parent=request.user)
        print(sick_leave_history, '-------------')
        serializer = ParentSickLeaveHistorySerializer(sick_leave_history, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Create a new Parent Sick Leave History.
        """
        serializer = ParentSickLeaveHistorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(parent=request.user)  # Automatically assign the logged-in user
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ToWhomItMayConcernCreateView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def post(self, request, *args, **kwargs):
        # Add the current authenticated user to the request data
        request.data['user'] = request.user.id

        # Deserialize the data sent in the request
        serializer = ToWhomItMayConcernSerializer(data=request.data)

        # Check if the data is valid
        if serializer.is_valid():
            # Save the new record to the database
            serializer.save()
            # Return a response indicating success
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # If data is not valid, return an error response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
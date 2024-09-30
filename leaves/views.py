from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from django.shortcuts import get_object_or_404
from .models import Leaves, CustomUser
from .serializers import LeavesSerializer
from rest_framework.permissions import IsAuthenticated

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

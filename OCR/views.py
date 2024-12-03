from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UploadedPDF
from children.models import Child
from .serializers import UploadedPDFSerializer

class ChildDocumentsAPIView(APIView):
    def get(self, request):
        # Extract query parameters
        child_id = request.query_params.get('child_id')
        category = request.query_params.get('category')
        print(child_id, '00000000000000')
        try:
            child = Child.objects.get(id=child_id)
        except Child.DoesNotExist:
            return Response({"error": "Child not found."}, status=status.HTTP_404_NOT_FOUND)
        print(child.UAE_number, '-------------',child.id )
        documents = UploadedPDF.objects.filter(urn_number=child.UAE_number)

        if category:
            documents = documents.filter(category=category)

        # Serialize and return the data
        serializer = UploadedPDFSerializer(documents, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

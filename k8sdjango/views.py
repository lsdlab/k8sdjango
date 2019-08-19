from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from apps.core.serializers import EmptySerializer


class IndexAPIView(APIView):
    permission_classes = (AllowAny, )
    serializer_class = EmptySerializer

    def get(self, request):
        return Response('pong', status=status.HTTP_200_OK)

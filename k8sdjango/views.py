from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from apps.core.serializers import EmptySerializer


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class IndexAPIView(APIView):
    permission_classes = (AllowAny, )
    serializer_class = EmptySerializer

    def get(self, request):
        return Response({'ping': 'pong'}, status=status.HTTP_200_OK)

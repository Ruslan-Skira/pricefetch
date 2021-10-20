from django.contrib.auth.models import Group, User
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from pricefetch.models import CurrencyExchangeRate
from pricefetch.serializers import FetchpriceSerializer, GroupSerializer, UserSerializer
from pricefetch.tasks import alphavantage_request


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class FetchPriceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows CurrencyExchangeRate to be viewed or edited.
    """
    queryset = CurrencyExchangeRate.objects.all()
    serializer_class = FetchpriceSerializer
    permission_classes = []

    def create(self, request: Request, *args, **kwargs) -> Response:
        """
        Method override base CreateModelMixin method.
        Add celery task for fetching data from API and adding it to request.data
        """

        try:
            serializer = alphavantage_request()  # data = fetch_price_alphavantage(request)
            serializer.is_valid()
        except UserWarning as e:
            return Response(e, status=status.HTTP_502_BAD_GATEWAY)
        return Response(serializer.validated_data, status=status.HTTP_502_BAD_GATEWAY)
        # return super().create(request, *args, **kwargs) # CurrencyExchangeRate.objects.create(**data); return Response(200)



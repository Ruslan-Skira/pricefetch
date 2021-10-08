from django.contrib.auth.models import Group, User
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from pricefetch.models import CurrencyExchangeRate
from pricefetch.serializers import FetchpriceSerializer, GroupSerializer, UserSerializer
from pricefetch.tasks import fetch_price_alphavantage


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
    """
     Create a model instance.
     """

    def create(self, request: Request, *args, **kwargs) -> Response:
        """
        Method override base CreateModelMixin method.
        Add celery task for fetching data from API and adding it to request.data
        :param request: Request parameter,
        :type request: Request
        :param args: additional argument
        :type args: list
        :param kwargs: additional arguments
        :type kwargs: dict
        :return: Response object with serialized data, status code and headers
        :rtype: Response
        """
        request._full_data = fetch_price_alphavantage(
            request.data)  # https://stackoverflow.com/questions/33861545/how-can-modify-request-data-in-django-rest-framework/45408337

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        # if fetch_price_alphavantage return response not 200 or return message error
        # return Response(serializer.data, status=status.HTTP_502_BAD_GATEWAY, headers=headers)

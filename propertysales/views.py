import datetime
import json
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from serializers import (
	TimeSeriesSerializer,
	TransactionHistoSerializer
)

from models import PropertySale

class TimeSeriesView(APIView):

	def get(self, request, format=None):
		property_sales = PropertySale.objects.values().order_by(
			'sale_date'
		)[:10]
		return Response(property_sales)

	def post(self, request, format=None):
		serializer = TimeSeriesSerializer(data=request.data)

		if serializer.is_valid():
			serializer.calc_mean_sale_price_time_series()
			response = serializer.get_mean_sale_price_time_series()
			response.update(serializer.data)
			return Response(json.dumps(response))

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HistogramView(APIView):

	def get(self, request, format=None):
		property_sales = PropertySale.objects.values().order_by(
			'sale_date'
		)[:10]
		return Response(property_sales)

	def post(self, request, format=None):
		serializer = TransactionHistoSerializer(data=request.data)

		if serializer.is_valid():
			serializer.calc_num_transactions_histogram()
			response = serializer.get_num_transactions_histogram()
			response.update(serializer.data)
			return Response(json.dumps(response))

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

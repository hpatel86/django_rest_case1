from datetime import datetime
import pandas as pd
import numpy as np

from rest_framework import serializers
from models import PropertySale
from const import PROPERTY_TYPES


class TimeSeriesSerializer(serializers.Serializer):

	"""Serializer to calculate the time seriese of average property sale
		per property type"""

	location = serializers.CharField(max_length=4)
	date_from = serializers.DateField(input_formats=['%B %Y'])
	date_to = serializers.DateField(input_formats=['%B %Y'])


	def calc_mean_sale_price_time_series(self):
		date_from = self.validated_data.get('date_from')
		date_to = self.validated_data.get('date_to')
		location = self.validated_data.get('location')

		queryset = PropertySale.objects.filter(
			sale_date__range=[date_from, date_to],
			postcode__startswith=location
		).order_by(
			'sale_date'
		).values(
			'sale_date',
			'sale_price',
			'property_type'
		)

		date_ranges = pd.date_range(date_from, date_to, freq='M')
		self.__sale_price_series = dict(
			description='Average Property Price Sold (to 100) Per Type',
			dates=date_ranges.map(lambda x: x.strftime('%B %Y')).tolist()
		)

		df = pd.DataFrame(list(queryset))
		for type_code, type_name in PROPERTY_TYPES:
			type_df = df[df['property_type']==type_code]
			type_df = type_df.set_index(pd.DatetimeIndex(type_df['sale_date']))
			g_type_df = type_df.groupby(pd.TimeGrouper('M')).mean().fillna(0)
			g_type_df['sale_price'] = g_type_df['sale_price']/100
			self.__sale_price_series[type_name] = [
				g_type_df.to_dict()['sale_price'].get(date, 0) for \
					date in date_ranges
			]


	def get_mean_sale_price_time_series(self):
		return self.__sale_price_series


class TransactionHistoSerializer(serializers.Serializer):
	""" Transaction histogram serializer """

	location = serializers.CharField(max_length=4, required=False)
	date = serializers.DateField(input_formats=['%B %Y'])


	def calc_num_transactions_histogram(self):
		date = self.validated_data.get('date')
		location = self.validated_data.get('location')

		queryset = PropertySale.objects.filter(
			sale_date__month=date.month,
			sale_date__year=date.year
		)

		if location is not None:
			queryset = queryset.filter(
				postcode__startswith=location
			)

		df = pd.DataFrame(list(queryset.values('sale_price')))
		bins = self._generate_bins(
			df['sale_price'].min(),
			df['sale_price'].max()
		)

		hist, _ = np.histogram(df['sale_price'], bins=bins)

		self.__histogram = dict(
			description='Number of Transactions Per Price Bracket',
			xvals=bins.tolist(),
			yvals=hist.tolist()
		)


	def get_num_transactions_histogram(self):
		return self.__histogram


	def _generate_bins(self, min_price, max_price):
		""" Default num bins to 8 and floor/ceil to nearest 10000"""

		min_price -= min_price % 10000 or 10000
		max_price += max_price % 10000 or 10000
		return np.linspace(min_price, max_price, 9)

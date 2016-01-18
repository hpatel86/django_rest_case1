from django.db import models
from const import (
	PROPERTY_TYPES,
	DURATION_TYPES,
)

class PropertySale(models.Model):
	postcode = models.CharField('PostCode', max_length=8, db_index=True)
	property_type = models.CharField(
		'Property Type',
		max_length=1,
		choices=PROPERTY_TYPES
	)
	sale_date = models.DateField('Date of Transfer', db_index=True)
	sale_price = models.PositiveIntegerField('Sale Price')
	duration = models.CharField(
		'Duration',
		max_length=1,
		choices=DURATION_TYPES
	)

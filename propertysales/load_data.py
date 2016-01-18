"""Migration script to load postgres DB"""

import sys
import os
import csv
import datetime

MIN_SALE_DATE = datetime.datetime(2010, 1, 1, 0, 0, 0)

sys.path.append('../')
os.environ['DJANGO_SETTINGS_MODULE'] = 'plentific_challenge.settings'

from propertysales.models import PropertySale

def usage():
	print '%s <csv_filepath>'%sys.argv[0]


def load_data(csv_file):
	with open(csv_file) as f:
		reader = csv.reader(f, delimiter=',')
		for i, row in enumerate(reader):
			sale_date = datetime.datetime.strptime(row[2], '%Y-%m-%d %H:%M')

			print i
			if sale_date <= MIN_SALE_DATE:
				continue

			prop_sale = PropertySale()
			prop_sale.property_type = row[4]
			prop_sale.postcode = row[3]
			prop_sale.sale_date = sale_date
			prop_sale.sale_price = row[1]
			prop_sale.duration = row[6]
			prop_sale.save()


if __name__ == '__main__':
	if len(sys.argv) != 2:
		usage()

	csv_file = sys.argv[1]
	load_data(csv_file)

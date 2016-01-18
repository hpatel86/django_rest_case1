from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

import views


urlpatterns = [
	url(r'^propertysale/timeseries/$', views.TimeSeriesView.as_view()),
	url(r'^propertysale/histogram/$', views.HistogramView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)

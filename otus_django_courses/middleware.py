import time

from django.utils.deprecation import MiddlewareMixin

from otus_django_courses.influxdb import InfluxLogger
from otus_django_courses.settings import env


class ResponseTimeMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if env('MONITORING'):
            request.start_time = time.time()

    def process_response(self, request, response):
        if not env('MONITORING'):
            return response

        total = time.time() - request.start_time
        InfluxLogger.write(measurement='django_response_time', value=total)
        return response

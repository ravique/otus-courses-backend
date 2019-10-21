import time

from django.utils.deprecation import MiddlewareMixin

from otus_django_courses.influxdb import InfluxLogger


class ResponseTimeMiddleware(MiddlewareMixin):

    def process_request(self, request):
        request.start_time = time.time()

    def process_response(self, request, response):
        total = time.time() - request.start_time
        InfluxLogger.write(measurement='django_response_time', value=total)
        return response

from rest_framework.views import APIView
from rest_framework.response import Response
import redis


class BuyStock(APIView):
    def post(self, request):
        user = request.data.get('user')
        stock_name = request.data.get('stockname')
        quantity = request.data.get('quantity')

        # Connect to Redis
        redis_host = 'localhost'
        redis_port = 6379
        redis_client = redis.Redis(host=redis_host, port=redis_port)

        # Check user credit in Redis
        user_credit = redis_client.hget(user, 'credit')

        if user_credit and int(user_credit) >= quantity:
            response_data = {'status': 'Accept'}
        else:
            response_data = {'status': 'Deny'}

        return Response(response_data)

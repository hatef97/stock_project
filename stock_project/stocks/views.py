from rest_framework.views import APIView
from rest_framework.response import Response
from django_redis import get_redis_connection
from .serializers import BuyStockSerializer


class BuyStock(APIView):
    def post(self, request):
        serializer = BuyStockSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        user = validated_data['user']
        stockname = validated_data['stockname']
        quantity = validated_data['quantity']

        # Connect to Redis database
        redis_conn = get_redis_connection()

        # Get user data from Redis
        user_data = redis_conn.hgetall(user)

        if not user_data:
            return Response({'message': 'User not found'}, status=400)

        user_credit = float(user_data.get('credit', 0))
        stock_price = float(redis_conn.get(stockname))

        required_credit = stock_price * quantity

        if user_credit >= required_credit:
            return Response({'message': 'Accept'}, status=200)
        else:
            return Response({'message': 'Deny'}, status=200)

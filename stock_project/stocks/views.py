from rest_framework.authtoken.admin import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException

from django_redis import get_redis_connection

from .serializers import BuyStockSerializer
from .tasks import verify_user


class BuyStockView(APIView):
    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
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

        self.notify_user(user_id)

        if not user_data:
            return Response({'message': 'User not found'}, status=400)

        user_credit = float(user_data.get('credit', 0))
        stock_price = float(redis_conn.get(stockname))

        required_credit = stock_price * quantity

        if user_credit >= required_credit:
            return Response({'message': 'Accept'}, status=200)
        else:
            return Response({'message': 'Deny'}, status=200)

        # Perform the verification asynchronously using Celery
        verify_user.delay(user_id)

        return Response({'message': 'Buy request received.'})

    def notify_user(self, user_id, notification_service=None):
        # Replace this with your actual implementation logic for notifying the user
        # For example, you can send a notification or update a status field in the user's record
        user = User.objects.get(id=user_id)  # Replace User with your actual user model
        user.notification = "Your buy request has been received."
        user.save()
        # Example: Sending a notification using a notification service or messaging system
        notification_service.send_notification(user_id, "Buy request received")

    def perform_verification(self, user_id):
        # Replace this with your actual implementation logic for user verification
        # For example, you can make an API call to an external service for verification
        # ...
        verification_result = 0  # Replace with your actual verification result
        if verification_result == 0:
            return True
        else:
            raise APIException("User verification failed.")

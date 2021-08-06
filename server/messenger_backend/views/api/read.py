from django.contrib.auth.middleware import get_user
from django.http import HttpResponse, JsonResponse
from messenger_backend.models import Conversation, Message
from online_users import online_users
from rest_framework.views import APIView


class Read(APIView):
    def put(self, request):
        try:
            user = get_user(request)

            if user.is_anonymous:
                return HttpResponse(status=401)

            body = request.data
            sender_id = body.get("senderId")
            conversation_id = body.get("conversationId")

            Message.objects.filter(senderId=sender_id).filter(conversation_id=conversation_id).filter(read=False).update(read=True)

            return JsonResponse({"message": "Updated unread messages"})
        except Exception as e:
            return HttpResponse(status=500)


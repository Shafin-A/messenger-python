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
            conversation_id = body.get("conversationId")

            conversation = Conversation.objects.get(id=conversation_id)
            sender_id = conversation.user1_id if user.id == conversation.user2_id else conversation.user2_id

            Message.objects.filter(senderId=sender_id).filter(conversation_id=conversation_id).filter(read=False).update(read=True)

            return JsonResponse({"message": "Updated unread messages"})
        except Exception as e:
            return HttpResponse(status=500)


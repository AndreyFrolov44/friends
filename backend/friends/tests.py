import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User
from users.serializers import UserSerializer
from .models import RequestFriend, Friend


class FriendTest(APITestCase):
    def setUp(self):
        self.jack = User.objects.create_user(username='jack', password='useruser')
        self.tom = User.objects.create_user(username='tom', password='useruser')

    def jack_sent_tom(self):
        self.client.force_authenticate(self.jack)
        return self.client.post(reverse('sent_request'), data={'username': 'tom'})

    def tom_sent_jack(self):
        self.client.force_authenticate(self.tom)
        return self.client.post(reverse('sent_request'), data={'username': 'jack'})    

    def test_sent_request_error_not_found(self):
        self.client.force_authenticate(self.jack)
        response = self.client.post(reverse('sent_request'), data={'username': 'tomtom'})

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_sent_request_error_self(self):
        self.client.force_authenticate(self.jack)
        response = self.client.post(reverse('sent_request'), data={'username': 'jack'})

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_sent_request_success(self):
        response = self.jack_sent_tom()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json.loads(response.content), {"status": "ok"})

    def test_sent_request_error_already_sent(self):
        response = self.jack_sent_tom()
        response = self.client.post(reverse('sent_request'), data={'username': 'tom'})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {"detail": "Request already sent"})

    def test_sent_success_reverse(self):
        response = self.tom_sent_jack()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json.loads(response.content), {"status": "ok"})

        response = self.jack_sent_tom()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json.loads(response.content), {"status": "ok"})

        self.assertEqual(RequestFriend.objects.count(), 0)
        self.assertEqual(self.jack.friend.friends.count(), 1)
        self.assertEqual(self.tom.friend.friends.count(), 1)

    def test_accept_request_error_not_sent(self):
        self.client.force_authenticate(self.tom)
        response = self.client.post(reverse('accept_request'), data={'username': 'jack'})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {'detail': 'This user has not sent you a friend request'})

    def test_accept_request_success(self):
        self.jack_sent_tom()

        self.client.force_authenticate(self.tom)
        response = self.client.post(reverse('accept_request'), data={'username': 'jack'})

        self.assertEqual(json.loads(response.content), {"status": "ok"})

        self.assertEqual(RequestFriend.objects.count(), 0)
        self.assertEqual(self.jack.friend.friends.count(), 1)
        self.assertEqual(self.tom.friend.friends.count(), 1)

    def test_reject_request_error_not_sent(self):
        self.client.force_authenticate(self.tom)
        response = self.client.post(reverse('reject_request'), data={'username': 'jack'})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {'detail': 'This user has not sent you a friend request'})

    def test_reject_request_success(self):
        self.jack_sent_tom()

        self.client.force_authenticate(self.tom)
        response = self.client.post(reverse('reject_request'), data={'username': 'jack'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), {'status': 'ok'})
        self.assertEqual(RequestFriend.objects.get(from_user=self.jack, to_user=self.tom).is_canceled, True)

    def test_outgoing_request_success(self):
        self.jack_sent_tom()

        self.client.force_authenticate(self.jack)
        response = self.client.get(reverse('outgoing_request'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), [{
                'id': RequestFriend.objects.get(from_user=self.jack, to_user=self.tom).id,
                'to_user': UserSerializer(self.tom).data, 
                'is_canceled': False
            }])
        
    def test_incoming_request_success(self):
        self.jack_sent_tom()

        self.client.force_authenticate(self.tom)
        response = self.client.get(reverse('incoming_request'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), [{
                'id': RequestFriend.objects.get(from_user=self.jack, to_user=self.tom).id,
                'from_user': UserSerializer(self.jack).data, 
                'is_canceled': False
            }])
        
    def test_friend_list_success(self):
        self.jack_sent_tom()
        self.tom_sent_jack()

        self.client.force_authenticate(self.tom)
        response = self.client.get(reverse('friend_list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), [UserSerializer(self.jack).data])

    def test_status(self):
        self.client.force_authenticate(self.tom)
        response = self.client.get(reverse('status'), data={'username': 'jack'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), {'status': None})

        self.jack_sent_tom()

        self.client.force_authenticate(self.tom)
        response = self.client.get(reverse('status'), data={'username': 'jack'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), {'status': 'Incoming request'})

        self.client.force_authenticate(self.jack)
        response = self.client.get(reverse('status'), data={'username': 'tom'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), {'status': 'Outgoing request'})

        self.tom_sent_jack()

        self.client.force_authenticate(self.jack)
        response = self.client.get(reverse('status'), data={'username': 'tom'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), {'status': 'Friends'})

        self.client.force_authenticate(self.tom)
        response = self.client.get(reverse('status'), data={'username': 'jack'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), {'status': 'Friends'})

    def test_delete_error(self):
        self.client.force_authenticate(self.tom)
        response = self.client.delete(reverse('friend_delete'), data={'username': 'jack'})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {"detail": "You are not friends"})

    def test_delete_error(self):
        self.tom_sent_jack()
        self.jack_sent_tom()

        self.client.force_authenticate(self.tom)
        response = self.client.delete(reverse('friend_delete'), data={'username': 'jack'})

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.jack.friend.friends.count(), 0)
        self.assertEqual(self.tom.friend.friends.count(), 0)


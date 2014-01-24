from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from django.utils import timezone
from models import Poll

import datetime

def create_poll(question, delta_hours):
    return Poll.objects.create(question=question, pub_date=timezone.now() + datetime.timedelta(hours=delta_hours))

class PollMethodTests(TestCase):
    def test_was_published_recently_with_future_poll(self):
        future_poll = Poll(question='Future', pub_date=timezone.now() + datetime.timedelta(days=30))
        self.assertEqual(future_poll.was_published_recently(), False)

    def test_was_published_recently_with_old_poll(self):
        old_poll = Poll(question='Old', pub_date=timezone.now() - datetime.timedelta(days=2))
        self.assertEqual(old_poll.was_published_recently(), False)

    def test_was_published_recently_with_recent_poll(self):
        recent_poll = Poll(question='Recent', pub_date=timezone.now() - datetime.timedelta(hours=5))
        self.assertEqual(recent_poll.was_published_recently(), True)

class PollIndexTests(TestCase):
    def test_index_view_with_no_polls(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls are available')
        self.assertQuerysetEqual(response.context['polls'], [])

    def test_index_view_with_a_past_poll(self):
        create_poll("Past poll", -720);
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['polls'], ['<Poll: Past poll>'])

    def test_index_view_with_a_future_poll(self):
        create_poll("Future poll", 720)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['polls'], [])

    def test_index_view_with_past_and_future_poll(self):
        create_poll("Past poll", -720)
        create_poll("Future poll", 720)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['polls'], ['<Poll: Past poll>'])

    def test_index_view_with_two_past_polls(self):
        create_poll("Past poll 1", -720)
        create_poll("Past poll 2", -1440)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['polls'], ['<Poll: Past poll 1>', '<Poll: Past poll 2>'])

class PollDetailTests(TestCase):
    def test_detail_view_with_a_future_poll(self):
        poll = create_poll("Future poll", 100)
        response = self.client.get(reverse('polls:detail', args=(poll.id, )))
        self.assertEqual(response.status_code, 404)

    def test_detail_view_with_a_past_poll(self):
        poll = create_poll("Past poll", -100)
        response = self.client.get(reverse('polls:detail', args=(poll.id, )))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Past poll")




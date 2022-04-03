from datetime import datetime

import pytest
from django.test import Client
from django.urls import reverse
from django.utils.timezone import make_aware

from fundraisers.models import Fundraiser, Comment


def _asset_sorted(db_list, view_list, reverse=True):
    view_list_ids = [view_object.id for view_object in view_list]
    db_sorted_list_ids = sorted([db_object.id for db_object in db_list], reverse=reverse)
    assert view_list_ids == db_sorted_list_ids


@pytest.mark.django_db
class TestFundraiserListView:
    def test_all_list(self, client: Client, fundraisers):
        response = client.get(reverse('fundraiser_list'))
        assert response.status_code == 200
        for fundraiser in fundraisers:
            assert fundraiser in response.context['object_list']
        _asset_sorted(fundraisers, response.context['object_list'])

    def test_all_list_empty(self, client: Client):
        response = client.get(reverse('fundraiser_list'))
        assert response.status_code == 200
        assert response.context['object_list'].count() == 0


@pytest.mark.django_db
class TestFundraiserCategoryListView:
    def test_category_list(self, client: Client, fundraisers, categories):
        for category in categories:
            response = client.get(reverse('fundraiser_category_list', kwargs={'slug': category.slug}))
            assert response.status_code == 200
            for fundraiser in fundraisers:
                if fundraiser.category == category:
                    assert fundraiser in response.context['object_list']
                else:
                    assert fundraiser not in response.context['object_list']

            _asset_sorted(
                [fundraiser for fundraiser in fundraisers if fundraiser.category == category],
                response.context['object_list']
            )

    def test_category_list_not_found(self, client: Client):
        response = client.get(reverse('fundraiser_category_list', kwargs={'slug': 'no-category'}))
        assert response.status_code == 404


@pytest.mark.django_db
class TestFundraiserDetailView:
    def test_detail(self, client: Client, fundraisers):
        for fundraiser in fundraisers:
            response = client.get(reverse('fundraiser_detail', kwargs={'pk': fundraiser.id}))
            assert response.status_code == 200
            assert fundraiser.id == response.context['object'].id

    def test_detail_not_found(self, client: Client):
        response = client.get(reverse('fundraiser_detail', kwargs={'pk': 999}))
        assert response.status_code == 404


@pytest.mark.django_db
class TestFundraiserMyListView:
    def test_not_logged_my_fundraisers_list(self, client: Client, fundraisers, users):
        response = client.get(reverse('fundraiser_my_list'))
        assert response.status_code == 302
        assert response.url.startswith(reverse('login'))

    def test_logged_my_list(self, client: Client, fundraisers, users):
        for user in users:
            client.force_login(user)
            response = client.get(reverse('fundraiser_my_list'))
            assert response.status_code == 200
            for fundraiser in fundraisers:
                if fundraiser.owner == user:
                    assert fundraiser in response.context['object_list']
                else:
                    assert fundraiser not in response.context['object_list']

            _asset_sorted(
                [fundraiser for fundraiser in fundraisers if fundraiser.owner == user],
                response.context['object_list']
            )


@pytest.mark.django_db
class TestFundraiserCreateView:
    def test_not_logged_fundraiser_create_get(self, client: Client, users):
        response = client.get(reverse('fundraiser_create'))
        assert response.status_code == 302
        assert response.url.startswith(reverse('login'))

    def test_not_logged_fundraiser_create_post(self, client: Client, users):
        response = client.post(reverse('fundraiser_create'))
        assert response.status_code == 302
        assert response.url.startswith(reverse('login'))

    def test_logged_fundraiser_create_get(self, client: Client, users):
        user = users[0]
        client.force_login(user)
        response = client.get(reverse('fundraiser_create'))
        assert response.status_code == 200

    def test_logged_fundraiser_create_post_valid(self, client: Client, users, categories):
        user = users[0]
        client.force_login(user)
        data = {
            'name': 'Test Fundraiser',
            'description': 'Test description',
            'category': categories[0].id,
            'purpose': 1000,
            'start_date': make_aware(datetime.strptime('2022-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')),
            'end_date': make_aware(datetime.strptime('2023-01-01 23:59:59', '%Y-%m-%d %H:%M:%S')),
        }
        response = client.post(reverse('fundraiser_create'), data)
        assert response.status_code == 302
        assert response.url.startswith(reverse('fundraiser_list'))
        Fundraiser.objects.get(**data)

    def test_logged_fundraiser_create_post_invalid(self, client: Client, users, categories):
        user = users[0]
        client.force_login(user)
        data = {
            'name': 'Test Fundraiser',
            'description': 'Test description',
        }
        response = client.post(reverse('fundraiser_create'), data)
        assert response.status_code == 200
        assert Fundraiser.objects.count() == 0


@pytest.mark.django_db
class TestFundraiserUpdateView:
    def test__not_logged__fundraiser__update__get(self, client: Client, users, fundraisers):
        response = client.get(reverse('fundraiser_update', kwargs={'pk': fundraisers[0].id}))
        assert response.status_code == 302
        assert response.url.startswith(reverse('login'))

    def test__not_logged__fundraiser__update__post(self, client: Client, users, fundraisers):
        response = client.get(reverse('fundraiser_update', kwargs={'pk': fundraisers[0].id}))
        assert response.status_code == 302
        assert response.url.startswith(reverse('login'))

    def test__logged__not_found_fundraiser__update__get(self, client: Client, users):
        user = users[0]
        client.force_login(user)
        response = client.get(reverse('fundraiser_update', kwargs={'pk': 768}))
        assert response.status_code == 404

    def test__logged__not_found_fundraiser__update__post(self, client: Client, users):
        user = users[0]
        client.force_login(user)
        response = client.post(reverse('fundraiser_update', kwargs={'pk': 768}))
        assert response.status_code == 404

    def test__logged__not_my_fundraiser__update__get(self, client: Client, users, fundraisers):
        user = users[0]
        client.force_login(user)
        not_my_fundraiser = [fundraiser for fundraiser in fundraisers if fundraiser.owner != user][0]
        response = client.get(reverse('fundraiser_update', kwargs={'pk': not_my_fundraiser.id}))
        assert response.status_code == 403

    def test__logged__not_my_fundraiser__update__post(self, client: Client, users, fundraisers):
        user = users[0]
        client.force_login(user)
        not_my_fundraiser = [fundraiser for fundraiser in fundraisers if fundraiser.owner != user][0]
        response = client.post(reverse('fundraiser_update', kwargs={'pk': not_my_fundraiser.id}))
        assert response.status_code == 403

    def test__logged__my_fundraiser__update__get(self, client: Client, users, fundraisers):
        user = users[0]
        client.force_login(user)
        my_fundraiser = [fundraiser for fundraiser in fundraisers if fundraiser.owner == user][0]
        response = client.get(reverse('fundraiser_update', kwargs={'pk': my_fundraiser.id}))
        assert response.status_code == 200

    def test__logged__my_fundraiser__update__post__valid(self, client: Client, fundraisers):
        my_fundraiser = fundraisers[0]
        user = my_fundraiser.owner
        client.force_login(user)
        data = {
            'name': 'Test Fundraiser 123',
            'description': 'Test description',
            'category': my_fundraiser.category.id,
            'purpose': 1000,
            'start_date': make_aware(datetime.strptime('2022-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')),
            'end_date': make_aware(datetime.strptime('2023-01-01 23:59:59', '%Y-%m-%d %H:%M:%S')),
        }
        response = client.post(reverse('fundraiser_update', kwargs={'pk': my_fundraiser.id}), data)
        assert response.status_code == 302
        assert response.url.startswith(reverse('fundraiser_update', kwargs={'pk': my_fundraiser.id}))
        Fundraiser.objects.get(**data)

    def test__logged__my_fundraiser__update__post__invalid(self, client: Client, fundraisers):
        my_fundraiser = fundraisers[0]
        user = my_fundraiser.owner
        client.force_login(user)
        data = {
            'name': 'Test Fundraiser 123',
            'description': 'Test description',
            'category': my_fundraiser.category.id,
            'purpose': 1000,
            'start_date': make_aware(datetime.strptime('2022-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')),
        }
        response = client.post(reverse('fundraiser_update', kwargs={'pk': my_fundraiser.id}), data)
        assert response.status_code == 200
        assert response.context['form'].errors['end_date'] == ['To pole jest wymagane.']
        assert Fundraiser.objects.filter(**data).count() == 0


@pytest.mark.django_db
class TestFundraiserCommentAddView:
    def test__not_existing_fundraiser__get(self, client: Client):
        response = client.get(reverse('fundraiser_comment_add', kwargs={'fundraiser_id': 768}))
        assert response.status_code == 405

    def test__not_existing_fundraiser__post(self, client: Client):
        response = client.post(reverse('fundraiser_comment_add', kwargs={'fundraiser_id': 768}))
        assert response.status_code == 404

    def test__existing_fundraiser__get(self, client: Client, fundraisers):
        fundraiser = fundraisers[0]
        response = client.get(reverse('fundraiser_comment_add', kwargs={'fundraiser_id': fundraiser.id}))
        assert response.status_code == 405

    def test__comment_form__shown(self, client: Client, fundraisers):
        fundraiser = fundraisers[0]
        client.force_login(fundraiser.owner)
        response = client.get(reverse('fundraiser_detail', kwargs={'pk': fundraiser.id}))
        assert response.status_code == 200
        assert response.context['comment_form'].fundraiser == fundraiser

    def test__not_logged__post__valid(self, client: Client, fundraisers):
        fundraiser = fundraisers[0]
        data = {
            'message': 'Test message',
        }
        response = client.post(reverse('fundraiser_comment_add', kwargs={'fundraiser_id': fundraiser.id}), data)
        assert response.status_code == 302
        assert response.url.startswith(reverse('fundraiser_detail', kwargs={'pk': fundraiser.id}))

        fundraiser.refresh_from_db()
        assert fundraiser.comment_set.count() == 1
        comment = fundraiser.comment_set.first()
        assert comment.message == data['message']
        assert comment.user is None

    def test__not_logged__post__invalid(self, client: Client, fundraisers):
        fundraiser = fundraisers[0]
        response = client.post(reverse('fundraiser_comment_add', kwargs={'fundraiser_id': fundraiser.id}), {})
        assert response.status_code == 302
        assert response.url.startswith(reverse('fundraiser_detail', kwargs={'pk': fundraiser.id}))
        assert Comment.objects.count() == 0

    def test__logged__post__valid(self, client: Client, fundraisers, users):
        user = users[0]
        fundraiser = fundraisers[0]
        client.force_login(user)
        data = {
            'message': 'Test message',
        }
        response = client.post(reverse('fundraiser_comment_add', kwargs={'fundraiser_id': fundraiser.id}), data)
        assert response.status_code == 302
        assert response.url.startswith(reverse('fundraiser_detail', kwargs={'pk': fundraiser.id}))

        fundraiser.refresh_from_db()
        assert fundraiser.comment_set.count() == 1
        comment = fundraiser.comment_set.first()
        assert comment.message == data['message']
        assert comment.user == user


@pytest.mark.django_db
class TestFundraiserVote:
    def test__not_existing_fundraiser__get(self, client: Client):
        response = client.get(reverse('fundraiser_vote', kwargs={'fundraiser_id': 768}))
        assert response.status_code == 405

    def test__not_existing_fundraiser__post(self, client: Client):
        response = client.post(reverse('fundraiser_vote', kwargs={'fundraiser_id': 768}))
        assert response.status_code == 404

    def test__existing_fundraiser__get(self, client: Client, fundraisers):
        fundraiser = fundraisers[0]
        response = client.get(reverse('fundraiser_vote', kwargs={'fundraiser_id': fundraiser.id}))
        assert response.status_code == 405

    def test_post__up(self, client: Client, fundraisers):
        fundraiser = fundraisers[0]
        data = {
            'vote': 'up',
        }
        response = client.post(reverse('fundraiser_vote', kwargs={'fundraiser_id': fundraiser.id}), data)
        assert response.status_code == 302
        assert response.url.startswith(reverse('fundraiser_detail', kwargs={'pk': fundraiser.id}))

        fundraiser.refresh_from_db()
        assert fundraiser.votes_positive == 1
        assert fundraiser.votes_negative == 0

    def test_post__down(self, client: Client, fundraisers):
        fundraiser = fundraisers[0]
        data = {
            'vote': 'down',
        }
        response = client.post(reverse('fundraiser_vote', kwargs={'fundraiser_id': fundraiser.id}), data)
        assert response.status_code == 302
        assert response.url.startswith(reverse('fundraiser_detail', kwargs={'pk': fundraiser.id}))

        fundraiser.refresh_from_db()
        assert fundraiser.votes_positive == 0
        assert fundraiser.votes_negative == 1

    def test_post__invalid(self, client: Client, fundraisers):
        fundraiser = fundraisers[0]
        data = {
            'vote': 'not set',
        }
        response = client.post(reverse('fundraiser_vote', kwargs={'fundraiser_id': fundraiser.id}), data)
        assert response.status_code == 302
        assert response.url.startswith(reverse('fundraiser_detail', kwargs={'pk': fundraiser.id}))

        fundraiser.refresh_from_db()
        assert fundraiser.votes_negative == 0
        assert fundraiser.votes_positive == 0


@pytest.mark.django_db
class TestFundraiserTransactionAddView:
    def test__not_existing_fundraiser__get(self, client: Client):
        response = client.get(reverse('fundraiser_transaction_add', kwargs={'fundraiser_id': 768}))
        assert response.status_code == 405

    def test__not_existing_fundraiser__post(self, client: Client):
        response = client.post(reverse('fundraiser_transaction_add', kwargs={'fundraiser_id': 768}))
        assert response.status_code == 404

    def test__existing_fundraiser__get(self, client: Client, fundraisers):
        fundraiser = fundraisers[0]
        response = client.get(reverse('fundraiser_transaction_add', kwargs={'fundraiser_id': fundraiser.id}))
        assert response.status_code == 405

    def test__comment_form__shown(self, client: Client, fundraisers):
        fundraiser = fundraisers[0]
        client.force_login(fundraiser.owner)
        response = client.get(reverse('fundraiser_detail', kwargs={'pk': fundraiser.id}))
        assert response.status_code == 200
        assert response.context['transaction_form'].fundraiser == fundraiser

    def test__not_logged__post__valid(self, client: Client, fundraisers):
        fundraiser = fundraisers[0]
        data = {
            'amount': '100',
            'comment': 'Test comment',
        }
        response = client.post(reverse('fundraiser_transaction_add', kwargs={'fundraiser_id': fundraiser.id}), data)
        assert response.status_code == 302
        assert response.url.startswith(reverse('fundraiser_detail', kwargs={'pk': fundraiser.id}))

        fundraiser.refresh_from_db()
        assert fundraiser.transaction_set.count() == 1
        transaction = fundraiser.transaction_set.first()
        assert transaction.comment == data['comment']
        assert transaction.amount == 100.00
        assert transaction.user is None

    def test__not_logged__post__invalid(self, client: Client, fundraisers):
        fundraiser = fundraisers[0]
        response = client.post(reverse('fundraiser_transaction_add', kwargs={'fundraiser_id': fundraiser.id}), {})
        assert response.status_code == 302
        assert response.url.startswith(reverse('fundraiser_detail', kwargs={'pk': fundraiser.id}))

        fundraiser.refresh_from_db()
        assert fundraiser.transaction_set.count() == 0

    def test__logged__post__valid(self, client: Client, fundraisers, users):
        user = users[0]
        fundraiser = fundraisers[0]
        client.force_login(user)
        data = {
            'amount': '100',
            'comment': 'Test comment',
        }
        response = client.post(reverse('fundraiser_transaction_add', kwargs={'fundraiser_id': fundraiser.id}), data)
        assert response.status_code == 302
        assert response.url.startswith(reverse('fundraiser_detail', kwargs={'pk': fundraiser.id}))

        fundraiser.refresh_from_db()
        assert fundraiser.transaction_set.count() == 1
        transaction = fundraiser.transaction_set.first()
        assert transaction.comment == data['comment']
        assert transaction.amount == 100.00
        assert transaction.user == user

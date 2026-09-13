from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from ..models import DictavoixDictionaryWord, DictavoixTheme


class DictavoixDictionaryTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_superuser(
            username="dictavoix-admin",
            email="dictavoix@example.com",
            password="password",
        )
        self.theme = DictavoixTheme.objects.create(name="Animaux")
        self.other_theme = DictavoixTheme.objects.create(name="Plantes")
        self.client.force_login(self.user)

    def test_dictionary_page_and_crud_api_are_theme_scoped(self):
        page_url = reverse("dictavoix:dictionary", args=[self.theme.pk])
        api_url = reverse("dictavoix:dictionary_api", args=[self.theme.pk])
        self.assertContains(self.client.get(page_url), "Dictionnaire : Animaux")

        create_response = self.client.post(
            api_url,
            {"word": "chat", "pronunciation_hint": "cha"},
            content_type="application/json",
        )
        self.assertEqual(create_response.status_code, 201)
        word_pk = create_response.json()["pk"]
        self.assertEqual(
            DictavoixDictionaryWord.objects.get(pk=word_pk).theme, self.theme
        )

        update_response = self.client.patch(
            api_url,
            {"pk": word_pk, "word": "chats", "pronunciation_hint": "cha"},
            content_type="application/json",
        )
        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(update_response.json()["word"], "chats")

        delete_response = self.client.delete(
            api_url,
            {"pk": word_pk},
            content_type="application/json",
        )
        self.assertEqual(delete_response.status_code, 200)
        self.assertFalse(DictavoixDictionaryWord.objects.filter(pk=word_pk).exists())

        other_api_url = reverse("dictavoix:dictionary_api", args=[self.other_theme.pk])
        response = self.client.post(
            other_api_url,
            {"word": "chat", "pronunciation_hint": "cha"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            DictavoixDictionaryWord.objects.get(pk=response.json()["pk"]).theme,
            self.other_theme,
        )

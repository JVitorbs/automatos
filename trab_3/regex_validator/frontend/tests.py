from django.test import Client, TestCase


class FrontendRoutesTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_index_get(self) -> None:
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Validador RegEx")

    def test_index_post_validate(self) -> None:
        response = self.client.post("/", {"data_type": "email", "value": "aluno@ufrn.br"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Resultado")

    def test_dashboard_page(self) -> None:
        response = self.client.get("/dashboard/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Dashboard")

    def test_history_page(self) -> None:
        response = self.client.get("/historico/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Historico")

    def test_export_page(self) -> None:
        response = self.client.get("/exportacao/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Exportacao")

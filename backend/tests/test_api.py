import unittest

from httpx import ASGITransport, AsyncClient

from backend.app.main import app, runs


class ApiTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        runs.clear()

    async def test_health_and_generation_step(self):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            health = client.get("/health")
            health = await health
            self.assertEqual(health.status_code, 200)
            self.assertEqual(health.json()["status"], "ok")

            created = await client.post("/api/runs", json={
                "population_size": 4,
                "generations": 2,
                "mutation_rate": 0.1,
                "seed": 492104,
                "initial_population": [1.45, 0.98, -1.25, -0.57],
            })
            self.assertEqual(created.status_code, 201)
            payload = created.json()
            self.assertEqual(payload["status"], "paused")
            self.assertEqual(payload["snapshot"]["bits"], 10)
            self.assertEqual(payload["snapshot"]["generation"], 0)

            stepped = await client.post(f"/api/runs/{payload['run_id']}/step")
            self.assertEqual(stepped.status_code, 200)
            self.assertEqual(stepped.json()["snapshot"]["generation"], 1)
            self.assertGreater(len(stepped.json()["snapshot"]["events"]), 2)

    async def test_invalid_population_is_rejected(self):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.post("/api/runs", json={
                "population_size": 4,
                "initial_population": [0.1, 0.2],
            })
            self.assertEqual(response.status_code, 422)


if __name__ == "__main__":
    unittest.main()

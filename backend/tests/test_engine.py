import unittest

from backend.app.engine import GeneticConfig, GeneticEngine


class GeneticEngineTests(unittest.TestCase):
    def test_guide_population_is_encoded_with_ten_bits(self):
        engine = GeneticEngine(GeneticConfig())
        self.assertEqual(engine.bits, 10)
        self.assertEqual([item.chromosome for item in engine.population], [
            "1010000101",
            "1001010110",
            "0101110111",
            "0110111011",
        ])

    def test_seed_makes_a_generation_reproducible(self):
        first = GeneticEngine(GeneticConfig(seed=77))
        second = GeneticEngine(GeneticConfig(seed=77))
        first.step()
        second.step()
        self.assertEqual(first.population_as_dicts(), second.population_as_dicts())
        self.assertEqual(
            [(event["phase"], event["inputs"], event["outputs"]) for event in first.events],
            [(event["phase"], event["inputs"], event["outputs"]) for event in second.events],
        )

    def test_step_emits_all_pedagogical_phases(self):
        engine = GeneticEngine(GeneticConfig(seed=1, generations=1))
        engine.step()
        phases = {event["phase"] for event in engine.events}
        self.assertTrue({"population", "evaluation", "selection", "crossover", "mutation", "replacement"}.issubset(phases))
        self.assertEqual(engine.generation, 1)
        self.assertEqual(engine.snapshot()["event_count"], len(engine.events))


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import math
import random
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from typing import Any


@dataclass(slots=True)
class GeneticConfig:
    lower_bound: float = -5.0
    upper_bound: float = 5.0
    precision: int = 2
    population_size: int = 4
    generations: int = 20
    mutation_rate: float = 0.10
    crossover_rate: float = 1.0
    seed: int = 492104
    initial_population: list[float] | None = None

    def validate(self) -> None:
        if self.lower_bound >= self.upper_bound:
            raise ValueError("El límite inferior debe ser menor que el superior.")
        if not 2 <= self.population_size <= 500:
            raise ValueError("La población debe contener entre 2 y 500 individuos.")
        if not 1 <= self.generations <= 10_000:
            raise ValueError("Las generaciones deben estar entre 1 y 10000.")
        if not 0 <= self.mutation_rate <= 1:
            raise ValueError("La probabilidad de mutación debe estar entre 0 y 1.")
        if not 0 <= self.crossover_rate <= 1:
            raise ValueError("La probabilidad de cruce debe estar entre 0 y 1.")
        if not 0 <= self.precision <= 6:
            raise ValueError("La precisión debe estar entre 0 y 6 decimales.")
        if self.initial_population and len(self.initial_population) != self.population_size:
            raise ValueError("La población inicial debe coincidir con el tamaño configurado.")


@dataclass(slots=True)
class Individual:
    id: str
    chromosome: str
    encoded: int
    x: float
    objective: float
    distance: float
    fitness: float
    probability: float = 0.0
    interval_start: float = 0.0
    interval_end: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["interval"] = f"[{self.interval_start:.4f}, {self.interval_end:.4f}{']' if self.interval_end >= 0.999999 else ')'}"
        return data


class GeneticEngine:
    """Reproducible binary genetic algorithm for f(x) = 1 - x²."""

    phases = ("population", "evaluation", "selection", "crossover", "mutation", "replacement", "summary")

    def __init__(self, config: GeneticConfig):
        config.validate()
        self.config = config
        self.random = random.Random(config.seed)
        self.scale = 10**config.precision
        self.domain_size = round((config.upper_bound - config.lower_bound) * self.scale) + 1
        self.bits = math.ceil(math.log2(self.domain_size))
        self.max_code = self.domain_size - 1
        self.generation = 0
        self.event_id = 0
        self.events: list[dict[str, Any]] = []
        self.convergence: list[dict[str, float | int]] = []
        self.population = self._initial_population()
        self._evaluate_population(self.population)
        self._emit(
            "population",
            "initial_population",
            "Población inicial codificada.",
            outputs={"population": self.population_as_dicts(), "bits": self.bits},
        )
        self._emit_evaluation_summary()

    def _initial_population(self) -> list[Individual]:
        if self.config.initial_population:
            values = self.config.initial_population
        elif self.config.population_size == 4 and self.config.lower_bound == -5 and self.config.upper_bound == 5:
            values = [1.45, 0.98, -1.25, -0.57]
        else:
            values = [
                self.random.uniform(self.config.lower_bound, self.config.upper_bound)
                for _ in range(self.config.population_size)
            ]
        return [self._individual_from_x(value, index + 1) for index, value in enumerate(values)]

    def encode(self, x: float) -> int:
        bounded = min(self.config.upper_bound, max(self.config.lower_bound, x))
        return max(0, min(self.max_code, round((bounded - self.config.lower_bound) * self.scale)))

    def decode(self, encoded: int) -> float:
        return round(self.config.lower_bound + encoded / self.scale, self.config.precision)

    def _individual_from_x(self, x: float, index: int) -> Individual:
        encoded = self.encode(x)
        return self._individual_from_code(encoded, index)

    def _individual_from_code(self, encoded: int, index: int) -> Individual:
        encoded = max(0, min(self.max_code, encoded))
        x = self.decode(encoded)
        objective = round(1 - x**2, max(4, self.config.precision + 2))
        distance = round(abs(1 - objective), max(4, self.config.precision + 2))
        fitness = round(1 / (1 + distance), 6)
        return Individual(
            id=f"i{index}",
            chromosome=format(encoded, f"0{self.bits}b"),
            encoded=encoded,
            x=x,
            objective=objective,
            distance=distance,
            fitness=fitness,
        )

    def _evaluate_population(self, population: list[Individual]) -> None:
        total = sum(item.fitness for item in population)
        cursor = 0.0
        for index, item in enumerate(population):
            item.probability = item.fitness / total if total else 1 / len(population)
            item.interval_start = cursor
            cursor = 1.0 if index == len(population) - 1 else cursor + item.probability
            item.interval_end = cursor

    def _select(self) -> tuple[Individual, float]:
        draw = self.random.random()
        selected = next((item for item in self.population if draw < item.interval_end), self.population[-1])
        return selected, draw

    def _cross(self, left: str, right: str) -> tuple[str, str, int | None, float]:
        draw = self.random.random()
        if draw >= self.config.crossover_rate:
            return left, right, None, draw
        point = self.random.randint(1, self.bits - 1)
        return left[:point] + right[point:], right[:point] + left[point:], point, draw

    def _mutate(self, chromosome: str) -> tuple[str, list[dict[str, float | int | str]]]:
        bits = list(chromosome)
        changes: list[dict[str, float | int | str]] = []
        for index, bit in enumerate(bits):
            draw = self.random.random()
            if draw < self.config.mutation_rate:
                new_bit = "0" if bit == "1" else "1"
                bits[index] = new_bit
                changes.append({"position": index + 1, "before": bit, "after": new_bit, "random": round(draw, 6)})
        return "".join(bits), changes

    def step(self) -> dict[str, Any]:
        if self.generation >= self.config.generations:
            return self.snapshot()
        self.generation += 1
        selected: list[Individual] = []
        selections: list[dict[str, Any]] = []
        for _ in range(self.config.population_size):
            individual, draw = self._select()
            selected.append(individual)
            selections.append({"random": round(draw, 6), "selected": individual.id, "interval": individual.to_dict()["interval"]})
        self._emit("selection", "roulette_selection", "Progenitores seleccionados mediante ruleta.", inputs={"draws": selections})

        child_codes: list[str] = []
        crossover_rows: list[dict[str, Any]] = []
        for offset in range(0, self.config.population_size, 2):
            parent_a = selected[offset]
            parent_b = selected[(offset + 1) % len(selected)]
            child_a, child_b, point, draw = self._cross(parent_a.chromosome, parent_b.chromosome)
            child_codes.extend((child_a, child_b))
            crossover_rows.append({
                "parents": [parent_a.chromosome, parent_b.chromosome],
                "children": [child_a, child_b],
                "point": point,
                "random": round(draw, 6),
            })
        child_codes = child_codes[: self.config.population_size]
        self._emit("crossover", "one_point_crossover", "Cruce de un punto aplicado.", outputs={"crossovers": crossover_rows})

        mutated_codes: list[str] = []
        mutation_rows: list[dict[str, Any]] = []
        for chromosome in child_codes:
            mutated, changes = self._mutate(chromosome)
            mutated_codes.append(mutated)
            mutation_rows.append({"before": chromosome, "after": mutated, "changes": changes})
        self._emit("mutation", "bit_flip_mutation", "Mutación evaluada bit por bit.", outputs={"mutations": mutation_rows})

        next_population = [
            self._individual_from_code(int(chromosome, 2), index + 1)
            for index, chromosome in enumerate(mutated_codes)
        ]
        self._evaluate_population(next_population)
        previous_best = max(self.population, key=lambda item: item.fitness)
        next_worst_index = min(range(len(next_population)), key=lambda index: next_population[index].fitness)
        if previous_best.fitness > next_population[next_worst_index].fitness:
            next_population[next_worst_index] = self._individual_from_code(previous_best.encoded, next_worst_index + 1)
            self._evaluate_population(next_population)
        self.population = next_population
        self._emit("replacement", "generational_replacement", "Nueva población evaluada con elitismo de un individuo.", outputs={"population": self.population_as_dicts()})
        self._emit_evaluation_summary()
        return self.snapshot()

    def run(self) -> dict[str, Any]:
        while self.generation < self.config.generations:
            self.step()
        return self.snapshot()

    def _emit_evaluation_summary(self) -> None:
        best = max(self.population, key=lambda item: item.fitness)
        mean = sum(item.fitness for item in self.population) / len(self.population)
        self.convergence.append({"generation": self.generation, "best": best.fitness, "mean": round(mean, 6)})
        self._emit(
            "evaluation",
            "population_evaluation",
            f"Generación {self.generation} evaluada. Mejor individuo: {best.id}.",
            objective_current=best.objective,
            objective_best=best.fitness,
            outputs={"best": best.to_dict(), "mean_fitness": round(mean, 6)},
        )

    def _emit(
        self,
        phase: str,
        operation: str,
        explanation: str,
        *,
        inputs: dict[str, Any] | None = None,
        outputs: dict[str, Any] | None = None,
        objective_current: float | None = None,
        objective_best: float | None = None,
    ) -> None:
        self.event_id += 1
        self.events.append({
            "event_id": self.event_id,
            "timestamp": datetime.now(UTC).isoformat(),
            "algorithm": "genetic",
            "level": "info",
            "phase": phase,
            "step_type": "generation",
            "step": self.generation,
            "operation": operation,
            "objective_current": objective_current,
            "objective_best": objective_best,
            "inputs": inputs or {},
            "outputs": outputs or {},
            "explanation": explanation,
        })

    def population_as_dicts(self) -> list[dict[str, Any]]:
        return [item.to_dict() for item in self.population]

    def snapshot(self) -> dict[str, Any]:
        best = max(self.population, key=lambda item: item.fitness)
        return {
            "generation": self.generation,
            "max_generations": self.config.generations,
            "bits": self.bits,
            "population": self.population_as_dicts(),
            "best": best.to_dict(),
            "convergence": self.convergence,
            "event_count": len(self.events),
        }

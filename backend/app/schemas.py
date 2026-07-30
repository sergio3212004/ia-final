from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, model_validator


class RunCreate(BaseModel):
    lower_bound: float = -5.0
    upper_bound: float = 5.0
    precision: int = Field(2, ge=0, le=6)
    population_size: int = Field(4, ge=2, le=500)
    generations: int = Field(20, ge=1, le=10_000)
    mutation_rate: float = Field(0.10, ge=0, le=1)
    crossover_rate: float = Field(1.0, ge=0, le=1)
    seed: int = 492104
    initial_population: list[float] | None = None
    auto_run: bool = False

    @model_validator(mode="after")
    def validate_bounds(self) -> "RunCreate":
        if self.lower_bound >= self.upper_bound:
            raise ValueError("lower_bound debe ser menor que upper_bound")
        if self.initial_population and len(self.initial_population) != self.population_size:
            raise ValueError("initial_population debe coincidir con population_size")
        return self


class RunCommandResponse(BaseModel):
    run_id: str
    status: Literal["paused", "running", "completed", "stopped", "failed"]
    snapshot: dict

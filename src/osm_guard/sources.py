"""Conservative *advisory* source-selection rules, not official service policy."""

from dataclasses import dataclass
from enum import Enum
import math


class Source(str, Enum):
    PUBLIC_OVERPASS = "bounded-overpass"
    LOCAL_EXTRACT = "local-pbf-extract"
    LOCAL_DATABASE = "local-database-or-managed-api"
    MAP_TILES = "policy-compatible-map-tiles"


@dataclass(frozen=True)
class Workload:
    workflow: str = "one-off"
    area_km2: float = 1.0
    daily_runs: int = 1
    users: int = 1
    needs_basemap: bool = False
    strict_sla: bool = False

    def __post_init__(self) -> None:
        if self.workflow not in {"one-off", "scheduled", "interactive", "bulk"}:
            raise ValueError("Invalid workflow. Choose one-off, scheduled, interactive, or bulk")
        if not math.isfinite(self.area_km2) or self.area_km2 <= 0 or self.daily_runs < 0 or self.users < 1:
            raise ValueError("Area must be > 0; daily runs >= 0; users >= 1")


@dataclass(frozen=True)
class Advice:
    source: Source
    reasons: tuple[str, ...]
    caveat: str = (
        "Advisory heuristics only. Verify the chosen operator's current rules, "
        "data freshness, attribution and ODbL obligations before deployment."
    )


def recommend(workload: Workload) -> Advice:
    """Return explainable conservative defaults. Not a general suitability guarantee."""
    if workload.needs_basemap:
        return Advice(Source.MAP_TILES, (
            "Basemap rendering requires a tile service, not a data-query API.",
            "Select a provider whose capacity and tile policy match expected traffic.",
        ))
    if workload.workflow == "interactive" or workload.users > 1 or workload.strict_sla:
        return Advice(Source.LOCAL_DATABASE, (
            "Multi-user or production traffic must not automatically hit public Overpass.",
            "Use a provisioned OSM-derived service or a local indexed dataset.",
        ))
    if workload.workflow in {"scheduled", "bulk"} or workload.area_km2 >= 100 or workload.daily_runs > 2:
        return Advice(Source.LOCAL_EXTRACT, (
            "Large or repeated tasks are better served from a locally stored extract.",
            "Use PBF ingestion plus an explicit update plan; do not redownload unnecessarily.",
        ))
    return Advice(Source.PUBLIC_OVERPASS, (
        "This appears to be a small, infrequent, one-off query.",
        "Bound the request, cache it, identify the client and obey instance-specific policy.",
    ))

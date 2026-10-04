import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    service_name: str = os.getenv("SERVICE_NAME", "observability-demo")
    slo_target: float = float(os.getenv("SLO_TARGET", "0.999"))

settings = Settings()

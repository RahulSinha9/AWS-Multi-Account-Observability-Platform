def error_budget(target: float) -> float:
    if not 0 < target <= 1:
        raise ValueError("target must be between 0 and 1")
    return 1 - target

def availability(successful: int, total: int) -> float:
    if total < 0 or successful < 0 or successful > total:
        raise ValueError("invalid request counts")
    if total == 0:
        return 1.0
    return successful / total

def burn_rate(target: float, observed: float) -> float:
    budget = error_budget(target)
    if budget == 0:
        return 0.0
    return (1 - observed) / budget

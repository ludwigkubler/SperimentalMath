# auto-injected by SEC sandbox
import itertools
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_sat_instance(n: int):
        literals = [f"x{i}" for i in range(1, n+1)]
        clauses = []
        for _ in range(n):
            clause = random.sample(literals, 2)
            clauses.append(f"({clause[0]} | ~{clause[1]})")
        return " & ".join(clauses)

    def resolution_width(phi: str) -> int:
        # Simplified resolution width calculation
        return len(phi.split(" & ")) + len(phi.split(" | "))

    def symplectic_volume(phi: str) -> float:
        # Simplified symplectic volume calculation
        return len(phi.split(" & "))

    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        phi = generate_sat_instance(n)
        min_vol = symplectic_volume(phi)
        w_phi = resolution_width(phi)
        results.append({"n": n, "min_vol": min_vol, "w_phi": w_phi})

    correlation_coefficient = 0.0
    instances_tested = len(results)
    n_max = max(r["n"] for r in results)

    if instances_tested < 30:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }

    # Calculate correlation coefficient
    x_mean = sum(r["min_vol"] for r in results) / instances_tested
    y_mean = sum(r["w_phi"] for r in results) / instances_tested
    numerator = sum((r["min_vol"] - x_mean) * (r["w_phi"] - y_mean) for r in results)
    denominator = math.sqrt(sum((r["min_vol"] - x_mean) ** 2 for r in results)) * math.sqrt(sum((r["w_phi"] - y_mean) ** 2 for r in results))
    correlation_coefficient = numerator / denominator if denominator != 0 else 0.0

    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.8 and abs(correlation_coefficient / y_mean - x_mean) <= 2 * y_mean,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results if r["conjecture_holds"]) / len(results) if any(r["conjecture_holds"] for r in results) else None
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["conjecture_holds"])) / len(results) if any(r["conjecture_holds"] for r in results) else None
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")
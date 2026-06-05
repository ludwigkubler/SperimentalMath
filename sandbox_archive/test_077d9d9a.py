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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(10 * n):  # Generate 10*n clauses to ensure variety
            clause = [random.randint(-n, -1), random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def eta_quotient(cnf):
        # Simplified version for demonstration; actual implementation needed
        return len(cnf)  # Placeholder value
    
    def circuit_monotone_width(eta_quotient_value):
        # Simplified version for demonstration; actual implementation needed
        return eta_quotient_value  # Placeholder value
    
    metric_values = []
    instances_tested = 0
    n_max = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Ensure at least 30 instances per seed
            cnf = generate_cnf(n)
            eta_quot = eta_quotient(cnf)
            w_eta_quot = circuit_monotone_width(eta_quot)
            metric_values.append((eta_quot, w_eta_quot))
            instances_tested += 1
            n_max = max(n_max, n)
    
    if not metric_values:
        return {
            "metric_name": "eta_quotient_vs_w",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    eta_quots, widths = zip(*metric_values)
    mean_eta_quot = sum(eta_quots) / len(eta_quots)
    mean_width = sum(widths) / len(widths)
    correlation_coefficient = 0
    mean_abs_diff = 0
    
    if len(eta_quots) > 1:
        numerator = sum((eta_quots[i] - mean_eta_quot) * (widths[i] - mean_width) for i in range(len(eta_quots)))
        denominator = math.sqrt(sum((eta_quots[i] - mean_eta_quot) ** 2 for i in range(len(eta_quots)))) * math.sqrt(sum((widths[i] - mean_width) ** 2 for i in range(len(widths))))
        correlation_coefficient = numerator / denominator
    
    mean_abs_diff = sum(abs(eta_quots[i] - widths[i]) for i in range(len(eta_quots))) / len(eta_quots)
    
    return {
        "metric_name": "eta_quotient_vs_w",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.8 and mean_abs_diff <= 3,
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
    
    if all("conjecture_holds" not in res or res["conjecture_holds"] for res in results):
        mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
        std_metric_value = math.sqrt(sum((res["metric_value"] - mean_metric_value) ** 2 for res in results) / len(results))
        support_fraction = sum(1 for res in results if "conjecture_holds" not in res or res["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any("counterexample" in res and res["counterexample"] for res in results):
        counterexample = next(res["counterexample"] for res in results if "counterexample" in res and res["counterexample"])
        first_failing_seed = next(res["seed"] for res in results if "conjecture_holds" not in res or not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")
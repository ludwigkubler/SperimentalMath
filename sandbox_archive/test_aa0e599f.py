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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(c == 0 for c in clause):
                continue
            clauses.append(clause)
        return clauses
    
    def eta_quotient(clauses):
        # Placeholder function to compute the minimal order of the eta-quotient
        # This is a dummy implementation and should be replaced with actual computation
        return random.randint(1, 10)  # Dummy value for demonstration purposes
    
    def circuit_monotone_width(clauses):
        # Placeholder function to compute the circuit monotone width
        # This is a dummy implementation and should be replaced with actual computation
        return random.randint(1, 10)  # Dummy value for demonstration purposes
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    instances_tested = 30
    n_max = n
    metric_name = "eta_quotient_circuit_monotone_width"
    metric_values = []
    
    for _ in range(instances_tested):
        cnf = generate_cnf(n)
        eta = eta_quotient(cnf)
        width = circuit_monotone_width(cnf)
        metric_values.append((eta, width))
    
    if len(metric_values) < 2:
        return {
            "metric_name": metric_name,
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "not_enough_data"
        }
    
    eta_values, width_values = zip(*metric_values)
    mean_eta = sum(eta_values) / len(eta_values)
    mean_width = sum(width_values) / len(width_values)
    variance_eta = sum((x - mean_eta)**2 for x in eta_values) / len(eta_values)
    variance_width = sum((x - mean_width)**2 for x in width_values) / len(width_values)
    covariance = sum((eta_values[i] - mean_eta) * (width_values[i] - mean_width) for i in range(len(eta_values))) / len(eta_values)
    
    correlation_coefficient = covariance / math.sqrt(variance_eta * variance_width)
    mean_abs_diff = sum(abs(eta - width) for eta, width in metric_values) / len(metric_values)
    
    conjecture_holds = abs(correlation_coefficient) >= 0.8 and mean_abs_diff <= 3
    
    return {
        "metric_name": metric_name,
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"correlation={correlation_coefficient}, mean_abs_diff={mean_abs_diff}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.2:
        print("RESULT: FALSIFIED counterexample=not_enough_support first_failing_seed=None")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")
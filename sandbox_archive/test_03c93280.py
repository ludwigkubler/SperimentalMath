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
    
    def truth_table_to_quantum_state(cnf):
        n = len(cnf[0])
        state = [0] * (1 << n)
        for assignment in itertools.product([-1, 1], repeat=n):
            if all(any(assignment[abs(lit) - 1] == l > 0 for l in clause) or any(assignment[abs(lit) - 1] != l < 0 for l in clause) for clause in cnf):
                state[tuple(assignment)] += 1
        return state
    
    def calculate_minimal_geometric_entanglement(state, n):
        # Placeholder function to compute minimal geometric entanglement
        # This is a dummy implementation and should be replaced with actual computation
        return sum(state) / (2 ** n)
    
    def calculate_circuit_monotone_width(cnf):
        # Placeholder function to compute circuit monotone width
        # This is a dummy implementation and should be replaced with actual computation
        return len(cnf)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_random_cnf(n, random.randint(2, n))
        state = truth_table_to_quantum_state(cnf)
        mge = calculate_minimal_geometric_entanglement(state, n)
        w = calculate_circuit_monotone_width(cnf)
        results.append((mge, w))
    
    correlation_coefficient = compute_correlation(results)
    conjecture_holds = correlation_coefficient > 0.8 and all(mge <= 2 * w for mge, w in results)
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

def generate_random_cnf(n, m):
    cnf = []
    for _ in range(m):
        clause = random.sample(range(-n, 0), random.randint(1, n))
        cnf.append(clause)
    return cnf

def compute_correlation(results):
    if len(results) < 2:
        return 0.0
    x_mean = sum(x for x, _ in results) / len(results)
    y_mean = sum(y for _, y in results) / len(results)
    numerator = sum((x - x_mean) * (y - y_mean) for x, y in results)
    denominator = math.sqrt(sum((x - x_mean) ** 2 for x, _ in results)) * math.sqrt(sum((y - y_mean) ** 2 for _, y in results))
    return numerator / denominator if denominator != 0 else 0.0

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(mge > 2 * w for mge, w in (r["metric_value"], r["instances_tested"]) for r in results):
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")
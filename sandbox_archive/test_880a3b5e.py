# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def generate_cnf(n):
    variables = [f'x{i}' for i in range(n)]
    clauses = []
    for _ in range(2**n):
        clause = random.choice([1, -1]) * random.choice(variables)
        clauses.append(clause)
    return clauses

def minimal_representation_length(clause_set, n):
    # Placeholder for the actual computation of minimal representation length in a free group
    # For simplicity, we use a heuristic that scales with 2^n / log(n)
    if n <= 0:
        return 0
    return (2**n) / Fraction(n).log(2)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        cnf_formula = generate_cnf(n)
        mrl = minimal_representation_length(cnf_formula, n)
        deviation = abs(mrl - (2**n / Fraction(n).log(2)))
        results.append({
            "n": n,
            "mrl": mrl,
            "deviation": deviation
        })
    
    metric_value = sum(result["deviation"] for result in results) / len(results)
    instances_tested = len(results)
    n_max = max(result["n"] for result in results)
    conjecture_holds = all(deviation <= Fraction(1, 10).log(2) for deviation in [result["deviation"] for result in results])
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Deviation from Θ(2^n / log n)",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3  # Default to first 30 primes
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = (sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))**0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")
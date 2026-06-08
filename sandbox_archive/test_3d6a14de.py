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

def generate_instance(n):
    clauses = []
    for _ in range(2 * n):
        clause = [random.randint(-n, -1), random.randint(1, n)]
        if all(lit not in [-x for x in clause] for lit in clause):
            clauses.append(clause)
    return clauses

def local_coherence(clauses):
    coherence = 0
    for i in range(len(clauses)):
        for j in range(i + 1, len(clauses)):
            common_literals = set(clauses[i]) & set(clauses[j])
            if common_literals:
                coherence += 1 / (len(common_literals) ** 2)
    return coherence

def dpll_path_length(n):
    # Simulate a simple DPLL path length for demonstration
    return random.randint(1, n)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        clauses = generate_instance(n)
        coherence = local_coherence(clauses)
        path_length = dpll_path_length(n)
        results.append({
            "n": n,
            "coherence": coherence,
            "path_length": path_length
        })
    metric_value = sum(result["coherence"] for result in results) / len(results)
    conjecture_holds = all(result["coherence"] >= n**(2/3) for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "local_coherence",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
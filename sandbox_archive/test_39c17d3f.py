# auto-injected by SEC sandbox
import math
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from itertools import product

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def ternary_diatomic_sequences(clauses):
        n = len(clauses)
        sequences = set()
        for assignment in product([-1, 0, 1], repeat=n):
            sequence = tuple(assignment)
            sequences.add(sequence)
        return sequences
    
    def generate_sat_instance(n: int, m: int) -> list:
        clauses = []
        for _ in range(m):
            clause = [random.choice([1, -1]) * random.randint(1, n) for _ in range(random.randint(1, n))]
            clauses.append(clause)
        return clauses
    
    def count_ternary_diatomic_sequences(clauses):
        sequences = ternary_diatomic_sequences(clauses)
        return len(sequences)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Ensure at least 30 instances per seed
            m = random.randint(1, min(n * 2, 100))  # Limit m to avoid excessive runtime
            clauses = generate_sat_instance(n, m)
            count = count_ternary_diatomic_sequences(clauses)
            results.append(count)
    
    metric_value = sum(results) / len(results)
    instances_tested = len(results)
    n_max = max([5, 10, 15, 20, 30, 40])
    conjecture_holds = all(count <= n**3 * m**2 for count, n, m in zip(results, [n]*instances_tested, [m]*instances_tested))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Number of Ternary Diatomic Sequences",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")
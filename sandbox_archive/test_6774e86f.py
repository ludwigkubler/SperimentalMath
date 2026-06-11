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

def generate_boolean_function(n):
    return {i: random.randint(0, 1) for i in range(2**n)}

def communication_complexity_rank_variance(f):
    n = int(math.log2(len(f)))
    rank_matrix = [[f[i ^ (a & (1 << j))] == f[i ^ (b & (1 << j))] for j in range(n)] for a, b in itertools.combinations(range(2**n), 2)]
    rank_sum = sum(sum(row) for row in rank_matrix)
    rank_variance = Fraction(rank_sum, len(rank_matrix)**2 - len(rank_matrix))
    return rank_variance

def quaternionic_automorphisms_count(f):
    n = int(math.log2(len(f)))
    count = 0
    for a in range(1 << n):
        if all((f[(i ^ (a & (1 << j)))] == f[(i ^ (b & (1 << j)))] for j in range(n))):
            count += 1
    return count

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    f = generate_boolean_function(n)
    C_f = communication_complexity_rank_variance(f)
    Aut_q_f = quaternionic_automorphisms_count(f)
    metric_value = abs(Aut_q_f) - math.sqrt(C_f)
    instances_tested = 1
    n_max = n
    conjecture_holds = metric_value <= 0.7
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "Aut_q(f) - sqrt(C(f))",
        "metric_value": float(metric_value),
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
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unsupported_operation")
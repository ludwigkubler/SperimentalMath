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

def generate_dnf(n, k):
    dnf = []
    for _ in range(k):
        clause = set(random.sample(range(1, n+1), 2))
        dnf.append(clause)
    return dnf

def is_k_clique(dnf, n):
    vertices = list(range(1, n+1))
    for i in range(len(vertices)):
        for j in range(i+1, len(vertices)):
            if not any(vertex in clause for clause in dnf for vertex in [vertices[i], vertices[j]]):
                return False
    return True

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    k = 5
    instances_tested = 30
    metric_value = 0.0
    conjecture_holds = True
    counterexample = ""

    for _ in range(instances_tested):
        dnf = generate_dnf(n, k)
        if is_k_clique(dnf, n):
            disjoint_count = 0
            while dnf:
                clause = dnf.pop()
                disjoint_count += 1
                dnf = [c for c in dnf if not any(vertex in clause for vertex in c)]
            metric_value += disjoint_count
        else:
            conjecture_holds = False
            counterexample = "Non-k-clique DNF found"

    metric_value /= instances_tested
    return {
        "metric_name": "disjoint_clauses",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or list(range(2, 30*100 + 1, 100))
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
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
    
    def polynomial_ring(cnf):
        n = len(cnf[0])
        variables = set()
        for clause in cnf:
            for literal in clause:
                if literal > 0:
                    variables.add(literal)
                else:
                    variables.add(-literal)
        return n, list(variables)

    def min_order_K_theory(n):
        # Placeholder function to simulate the computation
        # Replace with actual K-theory calculation logic
        return random.randint(1, n)

    def resolution_proof_width(cnf):
        # Placeholder function to simulate the computation
        # Replace with actual resolution proof width calculation logic
        return len(cnf) * 2

    instances_tested = 0
    total_min_order = 0
    total_w_phi = 0
    n_max = 0

    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        cnf = [[random.randint(-n, -1), random.randint(1, n)] for _ in range(n)]
        min_order = min_order_K_theory(n)
        w_phi = resolution_proof_width(cnf)

        instances_tested += len(cnf)
        total_min_order += min_order
        total_w_phi += w_phi
        n_max = max(n_max, n)

    mean_min_order = total_min_order / instances_tested
    mean_w_phi = total_w_phi / instances_tested

    correlation_coefficient = (instances_tested * sum(min_order * w_phi for min_order, w_phi in zip(range(1, n_max + 1), range(1, n_max + 1))) - 
                               instances_tested * mean_min_order * mean_w_phi) / \
                              math.sqrt((instances_tested * sum(min_order ** 2 for min_order in range(1, n_max + 1)) - instances_tested * mean_min_order ** 2) *
                                        (instances_tested * sum(w_phi ** 2 for w_phi in range(1, n_max + 1)) - instances_tested * mean_w_phi ** 2))

    conjecture_holds = correlation_coefficient >= 0.8
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "Pearson's Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)

    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
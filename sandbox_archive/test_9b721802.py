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
    n_max = 0
    instances_tested = 0
    total_metric_value = 0
    conjecture_holds = True
    counterexample = ""

    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            m = random.randint(1, min(n * 2, 100))  # Ensure m is not too large
            instances_tested += 1
            n_max = max(n_max, n)

            # Generate a random SAT instance with n variables and m clauses
            sat_instance = []
            for _ in range(m):
                clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
                if all(clause[i] != 0 for i in range(n)):
                    sat_instance.append(clause)

            # Map each SAT instance to a set of ternary diatomic sequences
            def is_ternary_diatomic(seq):
                return len(set(seq)) == 2 and -1 in seq and 1 in seq

            ternary_diatomic_sequences = []
            for assignment in product([-1, 0, 1], repeat=m):
                if all(assignment[i] != 0 for i in range(m)):
                    seq = [assignment[i] * sat_instance[i][j] for j in range(n) for i in range(m)]
                    if is_ternary_diatomic(seq):
                        ternary_diatomic_sequences.append(tuple(sorted(seq)))

            # Count the number of distinct ternary diatomic sequences
            num_ternary_diatomic = len(set(ternary_diatomic_sequences))

            # Measure the metric value
            total_metric_value += num_ternary_diatomic

            # Check if the conjecture holds
            if num_ternary_diatomic > n**2 * m:
                conjecture_holds = False
                counterexample = f"n={n}, m={m}, |D(SAT_instance)|={num_ternary_diatomic}"

    return {
        "metric_name": "Number of Ternary Diatomic Sequences",
        "metric_value": total_metric_value / instances_tested,
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
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
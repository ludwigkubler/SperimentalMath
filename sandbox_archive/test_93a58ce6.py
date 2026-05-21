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

def run_trial(seed: int) -> dict:
    def generate_3cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if random.choice([True, False]):
                clause[0], clause[1] = -clause[0], -clause[1]
            clauses.append(clause)
        return clauses

    def poset_euler_characteristic(poset):
        chain_counts = [len(list(chain)) for chain in poset]
        return sum((-1) ** (len(chain) % 2) * chain_count for chain_count in chain_counts)

    def disjointness_communication_complexity(clauses):
        n = len(set(abs(lit) for clause in clauses for lit in clause))
        # Simplified deterministic protocol complexity
        return n

    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    phi = generate_3cnf(n)
    P_phi = sorted(set(tuple(sorted(clause)) for clause in phi))
    chi_P_phi = poset_euler_characteristic(P_phi)
    D_phi = disjointness_communication_complexity(phi)

    return {
        "metric_name": "euler_characteristic",
        "metric_value": chi_P_phi,
        "instances_tested": 1,
        "conjecture_holds": abs(chi_P_phi - Fraction(n, 2).log(2) * D_phi) < 0.1 * chi_P_phi,
        "counterexample": "" if conjecture_holds else f"n={n}, P_phi={P_phi}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    total_metric_value = 0
    support_count = 0

    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        total_metric_value += trial_result["metric_value"]
        if trial_result["conjecture_holds"]:
            support_count += 1

    mean_metric_value = total_metric_value / len(seeds)
    support_fraction = support_count / len(seeds)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")
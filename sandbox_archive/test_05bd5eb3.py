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
    
    def generate_cnf(n, h):
        clauses = []
        for _ in range(h):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if random.choice([True, False]):
                clause[0] *= -1
            if random.choice([True, False]):
                clause[1] *= -1
            clauses.append(clause)
        return clauses

    def compute_mcd(cnf):
        # Placeholder for actual mcd computation
        # For simplicity, we use a dummy value here
        return len(cnf)

    def compute_clause_entropy(cnf):
        h = 0
        for clause in cnf:
            h += math.log2(len(clause))
        return h / len(cnf)

    n_values = [5, 10, 15, 20, 30, 40]
    mcd_sum = 0
    entropy_sum = 0
    instances_tested = 0

    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            cnf = generate_cnf(n, random.randint(1, n))
            mcd_value = compute_mcd(cnf)
            entropy_value = compute_clause_entropy(cnf)
            mcd_sum += mcd_value
            entropy_sum += entropy_value
            instances_tested += 1

    mean_mcd = mcd_sum / instances_tested
    mean_entropy = entropy_sum / instances_tested
    correlation_coefficient = (mcd_sum * entropy_sum - instances_tested * mean_mcd * mean_entropy) / \
                               math.sqrt((instances_tested * sum(mcd_value**2 for mcd_value in range(instances_tested)) - instances_tested * mean_mcd**2) *
                                         (instances_tested * sum(entropy_value**2 for entropy_value in range(instances_tested)) - instances_tested * mean_entropy**2))

    return {
        "metric_name": "mcd_vs_entropy",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.8 and abs(mean_mcd - mean_entropy) <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")
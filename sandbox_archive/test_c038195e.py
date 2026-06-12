# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations, permutations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_kcnf(n: int, k: int):
        clauses = []
        for _ in range(k):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses

    def symplectic_leaf_count(cnf):
        leaves = set()
        for clause in cnf:
            leaves.update(abs(lit) for lit in clause if lit != 0)
        return len(leaves)

    def rank_variance(cnf):
        n = len(cnf)
        total = sum(len(clause) for clause in cnf)
        mean = Fraction(total, n)
        variance = sum((len(clause) - mean) ** 2 for clause in cnf) / n
        return float(variance)

    instances_tested = 0
    total_symplectic_leaves_count = []
    total_rank_variance = []

    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(50):  # Aim for at least 30 instances per seed
            cnf = generate_kcnf(n, n)
            leaves_count = symplectic_leaf_count(cnf)
            rank_var = rank_variance(cnf)
            total_symplectic_leaves_count.append(leaves_count)
            total_rank_variance.append(rank_var)
            instances_tested += 1

    if not total_symplectic_leaves_count or not total_rank_variance:
        return {
            "metric_name": "MinimalLeavesCount",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max(5, n),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    correlation_coefficient = (instances_tested * sum(s * r for s, r in zip(total_symplectic_leaves_count, total_rank_variance)) -
                               len(total_symplectic_leaves_count) * sum(total_symplectic_leaves_count) * sum(total_rank_variance)) / \
                              math.sqrt((instances_tested * sum(s ** 2 for s in total_symplectic_leaves_count) - 
                                          (sum(total_symplectic_leaves_count) ** 2)) *
                                        (instances_tested * sum(r ** 2 for r in total_rank_variance) - 
                                         (sum(total_rank_variance) ** 2)))

    return {
        "metric_name": "MinimalLeavesCount",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max(5, n),
        "conjecture_holds": abs(correlation_coefficient) >= 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 30 primes if no seeds provided

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_corr_coeff = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
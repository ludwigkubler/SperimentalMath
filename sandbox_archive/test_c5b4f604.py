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
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(n):
            literals = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            clause = random.sample(literals, 3)
            clauses.append(clause)
        return clauses

    def configuration_space(clauses):
        n = len(clauses[0])
        space = []
        for assignment in itertools.product([0, 1], repeat=n):
            rank = 0
            for clause in clauses:
                if any(assignment[var - 1] == literal for literal in clause):
                    rank += 1
            space.append(rank)
        return space

    def min_rank(space):
        unique_ranks = set(space)
        return len(unique_ranks)

    n_values = [5, 10, 15, 20, 30, 40]
    results = []

    for n in n_values:
        clauses = generate_3cnf(n)
        space = configuration_space(clauses)
        rank = min_rank(space)
        log2_rank = math.log2(rank) if rank > 0 else -math.inf
        expected_bound = n / 3
        within_bound = abs(log2_rank - expected_bound) <= 1/3 * expected_bound

        results.append({
            "n": n,
            "rank": rank,
            "log2_rank": log2_rank,
            "expected_bound": expected_bound,
            "within_bound": within_bound
        })

    metric_value = sum(result["log2_rank"] for result in results) / len(results)
    instances_tested = len(results)
    conjecture_holds = all(result["within_bound"] for result in results)
    counterexample = "" if conjecture_holds else "n/3 bound not met"

    return {
        "metric_name": "log2(rank)",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30)) + list(map(lambda p: int(p), filter(str.isdigit, open("primes.txt").read().split())))
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_log_rank = sum(result["metric_value"] for result in results) / len(results)
    std_log_rank = math.sqrt(sum((result["metric_value"] - mean_log_rank) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_log_rank} std={std_log_rank} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n/3 bound not met\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")
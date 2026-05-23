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
    
    def generate_k_cnf(n, k):
        clauses = []
        for _ in range(k):
            clause = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            clauses.append(clause)
        return clauses

    def tropicalized_cohomology(cnf):
        # Simplified tropicalization logic
        cohomology = {}
        for clause in cnf:
            max_var = max(abs(var) for var in clause if var != 0)
            if max_var not in cohomology or len(clause) > len(cohomology[max_var]):
                cohomology[max_var] = len(clause)
        return cohomology

    def min_rank(tropicalized_cohomology):
        # Simplified rank calculation
        return sum(len(v) for v in tropicalized_cohomology.values())

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_k_cnf(n, random.randint(1, n))
        cohomology = tropicalized_cohomology(cnf)
        rank = min_rank(cohomology)
        results.append(rank)

    mean_rank = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean_rank) ** 2 for x in results) / len(results))

    conjecture_holds = all(rank <= n for rank, n in zip(results, n_values))
    counterexample = "" if conjecture_holds else f"n={n}, rank={rank}"

    return {
        "metric_name": "min_rank",
        "metric_value": mean_rank,
        "instances_tested": len(n_values),
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
    std_dev = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={n}, rank={rank}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")
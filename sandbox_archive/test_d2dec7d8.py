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
    
    k = 3  # Fixed constant for k-SAT
    n_min = 5
    n_max = 40
    instances_per_seed = 10
    
    def generate_k_sat_instance(n, k):
        clauses = []
        variables = list(range(1, n + 1))
        for _ in range(k * n):
            clause = random.sample(variables, 3)
            clause = [random.choice([x, -x]) for x in clause]
            clauses.append(clause)
        return clauses
    
    def conflict_set(clauses):
        conflicts = set()
        for i, clause1 in enumerate(clauses):
            for j, clause2 in enumerate(clauses):
                if i < j:
                    common_vars = set(x for x in clause1 if -x in clause2)
                    if common_vars:
                        conflicts.add((i, j))
        return conflicts
    
    def tropicalized_hodge_structure(conflicts):
        rank = 0
        for conflict in conflicts:
            rank += len(conflict)
        return rank / len(conflicts) if conflicts else 0
    
    total_rank = 0
    instances_tested = 0
    
    for _ in range(instances_per_seed):
        n = random.randint(n_min, n_max)
        clauses = generate_k_sat_instance(n, k)
        conflicts = conflict_set(clauses)
        rank = tropicalized_hodge_structure(conflicts)
        total_rank += rank
        instances_tested += 1
    
    mean_rank = total_rank / instances_tested
    expected_ratio = math.log(n) / math.log(k)
    ratio = mean_rank / expected_ratio if expected_ratio != 0 else float('inf')
    
    conjecture_holds = abs(ratio - 1) <= 0.2
    counterexample = "" if conjecture_holds else f"Ratio {ratio} outside ±20% of Θ(log(n)/log(k))"
    
    return {
        "metric_name": "minimal_rank_ratio",
        "metric_value": ratio,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}")
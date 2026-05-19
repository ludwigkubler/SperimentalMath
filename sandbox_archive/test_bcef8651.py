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
    
    def generate_dnf(n, k):
        clauses = []
        for _ in range(k):
            clause = set(random.sample(range(1, n+1), random.randint(1, n)))
            clauses.append(clause)
        return clauses
    
    def is_k_clique(dnf, n):
        for i in range(n):
            for j in range(i + 1, n):
                if not any(i in clause and j in clause for clause in dnf):
                    return False
        return True
    
    def max_pairwise_disjoint_clauses(dnf):
        disjoint_clauses = []
        for clause in dnf:
            if all(not (disjoint_clause & clause) for disjoint_clause in disjoint_clauses):
                disjoint_clauses.append(clause)
        return len(disjoint_clauses)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        if is_k_clique(generate_dnf(n, k), n):
            max_disjoint = max_pairwise_disjoint_clauses(generate_dnf(n, n))
            results.append(max_disjoint)
        else:
            max_disjoint = max_pairwise_disjoint_clauses(generate_dnf(n, 10))
            results.append(max_disjoint)
    
    if len(results) < 30:
        return {
            "metric_name": "max_disjoint_clauses",
            "metric_value": sum(results) / len(results),
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    mean = sum(results) / len(results)
    std = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for x in results if x >= n // 2) / len(results)
    
    return {
        "metric_name": "max_disjoint_clauses",
        "metric_value": mean,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean = sum(result["metric_value"] for result in results) / len(results)
    std = math.sqrt(sum((result["metric_value"] - mean) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not_enough_disjoint_clauses\" first_failing_seed={first_failing_seed}")
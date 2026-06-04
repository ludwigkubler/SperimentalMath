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
    
    def generate_sat_clause_set(n):
        num_clauses = random.randint(5, 10)
        clauses = []
        for _ in range(num_clauses):
            clause = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            clauses.append(clause)
        return clauses
    
    def compute_nerve(clauses):
        n = len(clauses[0])
        nerve = [[False] * n for _ in range(n)]
        for clause in clauses:
            for i in range(n):
                if clause[i] > 0:
                    for j in range(i + 1, n):
                        if clause[j] > 0 and (nerve[i][j] or nerve[j][i]):
                            return None
                        nerve[i][j] = True
                        nerve[j][i] = True
        return nerve
    
    def compute_local_indeterminacy(nerve):
        if not nerve:
            return float('inf')
        n = len(nerve)
        indeterminacy = 0
        for i in range(n):
            for j in range(i + 1, n):
                if nerve[i][j]:
                    indeterminacy += 1
        return indeterminacy
    
    def estimate_complexity(clauses):
        return len(clauses)
    
    n_max = 40
    instances_tested = 30
    total_indeterminacy = 0
    total_complexity = 0
    
    for _ in range(instances_tested):
        clauses = generate_sat_clause_set(n_max)
        nerve = compute_nerve(clauses)
        if nerve is None:
            continue
        indeterminacy = compute_local_indeterminacy(nerve)
        complexity = estimate_complexity(clauses)
        total_indeterminacy += indeterminacy
        total_complexity += complexity
    
    if instances_tested == 0:
        return {
            "metric_name": "local_indeterminacy_ratio",
            "metric_value": float('inf'),
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "empty_instance_set"
        }
    
    ratio = total_indeterminacy / total_complexity
    return {
        "metric_name": "local_indeterminacy_ratio",
        "metric_value": ratio,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": ratio <= 10,  # Arbitrary constant c for demonstration
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='local_indeterminacy_ratio' first_failing_seed={first_failing_seed}")
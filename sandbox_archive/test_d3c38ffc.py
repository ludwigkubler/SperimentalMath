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

def generate_random_sat_instance(n, m):
    clauses = []
    for _ in range(m):
        clause = [random.randint(1, n), random.randint(-n, -1)]
        clauses.append(clause)
    return clauses

def compute_permutation(clauses, n):
    perm = list(range(1, n + 1))
    for clause in clauses:
        if clause[0] > 0 and clause[1] < 0:
            i, j = abs(clause[0]) - 1, abs(clause[1]) - 1
            perm[i], perm[j] = perm[j], perm[i]
    return perm

def coxeter_group_action(perm, x):
    n = len(x)
    result = [0] * n
    for i in range(n):
        result[perm[i]] = x[i]
    return result

def count_distinct_minimal_invariants(clauses, n):
    m = len(clauses)
    if m == 0:
        return 0
    
    perm = compute_permutation(clauses, n)
    x = [i for i in range(1, n + 1)]
    
    def is_invariant(y):
        y_prime = coxeter_group_action(perm, y)
        return all(y[i] == y_prime[i] for i in range(n))
    
    min_invariants = set()
    queue = [tuple(x)]
    visited = {tuple(x)}
    
    while queue:
        current = queue.pop(0)
        if is_invariant(current):
            min_invariants.add(tuple(current))
        
        for i in range(n):
            for j in range(i + 1, n):
                new_y = list(current)
                new_y[i], new_y[j] = new_y[j], new_y[i]
                new_y_tuple = tuple(new_y)
                if new_y_tuple not in visited:
                    visited.add(new_y_tuple)
                    queue.append(new_y_tuple)
    
    return len(min_invariants)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        m = random.randint(1, min(2 * n, 50))
        clauses = generate_random_sat_instance(n, m)
        
        if not clauses:
            continue
        
        instances_tested += len(clauses)
        num_invariants = count_distinct_minimal_invariants(clauses, n)
        total_metric_value += num_invariants
        n_max = max(n_max, n)
        
        if num_invariants > 0.5 * n ** 0.5:
            conjecture_holds = False
            counterexample = f"n={n}, invariants={num_invariants}"
    
    metric_name = "number_of_distinct_minimal_invariants"
    metric_value = total_metric_value / instances_tested if instances_tested > 0 else 0
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
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
    std_metric_value = (sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
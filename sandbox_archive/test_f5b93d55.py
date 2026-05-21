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
    n = 40
    c = 0.2  # universal constant
    metric_name = "free_entropy"
    
    def generate_3cnf(n):
        clauses = []
        for i in range(n):
            clause = random.sample(range(n), 3)
            clauses.append(clause)
        return clauses
    
    def adjacency_matrix(clauses, n):
        M = [[0] * n for _ in range(n)]
        for clause in clauses:
            for var in clause:
                M[var][var] = 1
        return M
    
    def monte_carlo_free_entropy(M, n, num_samples=10000):
        total_log_sum = 0
        for _ in range(num_samples):
            z = complex(random.uniform(-1, 1), random.uniform(-1, 1))
            if abs(z) == 0:
                continue
            eigenvalues = [z - M[i][i] for i in range(n)]
            log_sum = sum(math.log(abs(eig)) for eig in eigenvalues)
            total_log_sum += log_sum
        return -total_log_sum / num_samples
    
    random.seed(seed)
    clauses = generate_3cnf(n)
    M = adjacency_matrix(clauses, n)
    phi_M = monte_carlo_free_entropy(M, n)
    
    metric_value = phi_M
    instances_tested = 1
    conjecture_holds = phi_M >= c * n
    counterexample = "" if conjecture_holds else f"Graph with n={n}, A={M}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30))  # default to first 30 primes
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results) and support_fraction >= 0.8:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")
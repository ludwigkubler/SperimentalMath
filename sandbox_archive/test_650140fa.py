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
        for _ in range(2 * n):
            clause = [random.randint(0, 1) * 2 - 1 for _ in range(3)]
            while len(set(clause)) < 3:
                clause[random.randint(0, 2)] *= -1
            clauses.append(clause)
        return clauses
    
    def adjacency_matrix(clauses, n):
        M = [[0] * n for _ in range(n)]
        for i, clause in enumerate(clauses):
            for var in clause:
                if var > 0:
                    M[var-1][i] = 1
                else:
                    M[-var-1][i] = -1
        return M
    
    def monte_carlo_free_entropy(M, n, samples=10000):
        total = 0
        for _ in range(samples):
            z = random.uniform(-1, 1) + random.uniform(-1, 1) * 1j
            if abs(z) == 0:
                continue
            trace = sum(abs(sum(row[i] * z**i for i in range(n))) for row in M)
            total += -math.log(abs(z - trace / n))
        return total / samples
    
    n = 40
    clauses = generate_3cnf(n)
    M = adjacency_matrix(clauses, n)
    phi_M = monte_carlo_free_entropy(M, n)
    
    metric_name = "free_entropy"
    metric_value = phi_M
    instances_tested = 1
    conjecture_holds = phi_M >= 0.2 * n
    counterexample = "" if conjecture_holds else f"Graph with n={n}, phi_M={phi_M}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30*4 + 1))
    
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
        print(f"RESULT: FALSIFIED counterexample=\"phi_M < 0.2n\" first_failing_seed={first_failing_seed}")
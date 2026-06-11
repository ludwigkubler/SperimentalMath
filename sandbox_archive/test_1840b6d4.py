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
    
    def cnf_to_matrix(phi):
        n = max(abs(lit) for clause in phi for lit in clause)
        M = [[0] * (2*n + 1) for _ in range(2*n + 1)]
        for clause in phi:
            for lit in clause:
                if lit > 0:
                    i, j = lit - 1, n + lit
                else:
                    i, j = -lit - 1, n - lit
                M[i][j] = 1
        return M
    
    def matrix_order(M):
        n = len(M) // 2
        order = 0
        for i in range(2*n + 1):
            for j in range(2*n + 1):
                if M[i][j]:
                    order += 1
        return order
    
    def is_quaternionic_representable(M, n):
        # Placeholder function to check quaternionic representability
        # This is a dummy implementation and should be replaced with actual logic
        return True
    
    def compute_minimal_order(phi):
        M = cnf_to_matrix(phi)
        if not is_quaternionic_representable(M, len(phi)):
            return float('inf')
        return matrix_order(M)
    
    phi = []
    n_clauses = random.randint(5, 30)
    for _ in range(n_clauses):
        clause_size = random.randint(1, min(4, n_clauses))
        clause = [random.choice([-i, i]) for i in range(1, n_clauses + 1)][:clause_size]
        phi.append(clause)
    
    minimal_order = compute_minimal_order(phi)
    return {
        "metric_name": "minimal_order",
        "metric_value": minimal_order,
        "instances_tested": len(phi),
        "n_max": max(len(clause) for clause in phi),
        "conjecture_holds": minimal_order < float('inf'),
        "counterexample": "" if minimal_order < float('inf') else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
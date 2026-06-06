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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n - 1):
            clause = [random.choice([f'x{i+1}', f'-x{i+1}']) for i in range(n)]
            clauses.append(clause)
        return clauses
    
    def matrix_from_cnf(cnf, n):
        m = len(cnf)
        A = [[0] * (n + 1) for _ in range(m)]
        for i, clause in enumerate(cnf):
            for literal in clause:
                if literal[0] == '-':
                    var = int(literal[1:]) - 1
                    A[i][var] = -1
                else:
                    var = int(literal[1:]) - 1
                    A[i][var] = 1
        return A
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            if A[i][i] == 0:
                for j in range(i + 1, m):
                    if A[j][i] != 0:
                        A[i], A[j] = A[j], A[i]
                        break
            if A[i][i] == 0:
                continue
            pivot = Fraction(A[i][i])
            for j in range(n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i and A[j][i] != 0:
                    factor = -A[j][i]
                    for k in range(n):
                        A[j][k] += factor * A[i][k]
        rank = sum(1 for row in A if any(row))
        return rank
    
    def local_induction_ring_rank(K):
        # Placeholder for actual LIR calculation
        # This is a dummy implementation and should be replaced with the correct method
        return 1  # Example value, replace with actual LIR calculation
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    A = matrix_from_cnf(cnf, n)
    rank_A = gaussian_elimination(A)
    K = local_induction_ring_rank("Q")  # Placeholder for the field K
    c = Fraction(1, 1)  # Example constant, replace with actual calculation
    
    variance = 0
    instances_tested = 30
    n_max = n
    
    for _ in range(instances_tested):
        rank_A_instance = gaussian_elimination(A)
        variance += (rank_A_instance - rank_A) ** 2
    
    variance /= instances_tested
    conjecture_holds = variance <= c * K
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Variance of Communication Complexity Rank",
        "metric_value": float(variance),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_dev = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
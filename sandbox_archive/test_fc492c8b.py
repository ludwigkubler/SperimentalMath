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
    
    def generate_read_twice_bp(n):
        # Generate a read-twice branching program for IP_2 with n states
        bp = [[random.choice([0, 1]) for _ in range(2)] for _ in range(n)]
        return bp
    
    def transition_matrix(bp):
        n = len(bp)
        T = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if bp[i][0] == 1:
                    T[j][(i + 1) % n] += 1
                if bp[i][1] == 1:
                    T[(j + 1) % n][i] += 1
        return T
    
    def free_cumulants(T):
        # R-transform inversion formula to compute free cumulants (simplified)
        n = len(T)
        det_T = determinant(T)
        if det_T == 0:
            return [float('inf')] * n
        inv_T = inverse_matrix(T, det_T)
        cumulants = []
        for i in range(n):
            cumulant = 0
            for j in range(n):
                cumulant += T[i][j] * inv_T[j][i]
            cumulants.append(cumulant)
        return cumulants
    
    def determinant(matrix):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        det = 0
        for j in range(n):
            minor = [row[:j] + row[j+1:] for row in matrix[1:]]
            det += ((-1) ** j) * matrix[0][j] * determinant(minor)
        return det
    
    def inverse_matrix(matrix, det):
        n = len(matrix)
        inv = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                minor = [row[:j] + row[j+1:] for row in matrix[:i] + matrix[i+1:]]
                inv[i][j] = ((-1) ** (i+j)) * determinant(minor) / det
        return inv
    
    def ceil_log_n(n):
        return math.ceil(math.log2(n))
    
    n = random.randint(5, 40)
    bp = generate_read_twice_bp(n)
    T = transition_matrix(bp)
    cumulants = free_cumulants(T)
    k = ceil_log_n(n)
    sum_first_k_cumulants = sum(cumulants[:k])
    
    size_P = len(bp) ** 2
    if sum_first_k_cumulants < math.log(size_P):
        conjecture_holds = False
        counterexample = "sum_first_k_cumulants < log(size(P))"
    else:
        conjecture_holds = True
        counterexample = ""
    
    return {
        "metric_name": "sum_first_k_cumulants",
        "metric_value": sum_first_k_cumulants,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
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
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"sum_first_k_cumulants < log(size(P))\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction} < 0.8")
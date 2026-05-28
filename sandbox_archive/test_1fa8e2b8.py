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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def quadratic_form_matrix(f):
        n = int(math.log2(len(f)))
        M = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                count = 0
                for x in range(2**n):
                    if f[x ^ (1 << i)] != f[x ^ (1 << j)]:
                        count += 1
                M[i][j] = M[j][i] = Fraction(count, 2**(n-1))
        return M
    
    def min_rank(matrix):
        n = len(matrix)
        A = [row[:] for row in matrix]
        rank = 0
        for i in range(n):
            if all(A[i][j] == 0 for j in range(i, n)):
                continue
            pivot_col = next(j for j in range(i, n) if A[i][j] != 0)
            for j in range(pivot_col, n):
                A[i][j] /= A[i][pivot_col]
            rank += 1
            for k in range(n):
                if k == i:
                    continue
                factor = A[k][pivot_col]
                for j in range(pivot_col, n):
                    A[k][j] -= factor * A[i][j]
        return rank
    
    def communication_complexity(f):
        n = int(math.log2(len(f)))
        # Simplified Forster's signed-rank technique
        count = 0
        for x in range(2**n):
            if f[x ^ (1 << 0)] != f[x]:
                count += 1
        return Fraction(count, 2**(n-1))
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        f = generate_boolean_function(n)
        M_f = quadratic_form_matrix(f)
        tau_quad = min_rank(M_f)
        comm_complexity = communication_complexity(f)
        
        if tau_quad == 0 or comm_complexity == 0:
            continue
        
        results.append({
            "n": n,
            "tau_quad": tau_quad,
            "comm_complexity": comm_complexity
        })
    
    if not results:
        return {
            "metric_name": "communication_complexity",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances found"
        }
    
    total_comm = sum(result["comm_complexity"] for result in results)
    avg_comm = Fraction(total_comm, len(results))
    max_comm = max(result["comm_complexity"] for result in results)
    
    conjecture_holds = all(avg_comm >= 0.9 * tau_quad / (n * math.log(n)) and comm <= 1.2 * tau_quad
                           for result in results for n, tau_quad, comm in [(result["n"], result["tau_quad"], result["comm_complexity"])]
                           if tau_quad != 0 and comm != 0)
    
    counterexample = ""
    if not conjecture_holds:
        for result in results:
            n, tau_quad, comm = result["n"], result["tau_quad"], result["comm_complexity"]
            if avg_comm < 0.7 * tau_quad / (n * math.log(n)) or comm > 1.5 * tau_quad:
                counterexample = f"n={n}, tau_quad={tau_quad}, comm={comm}"
                break
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": avg_comm,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    avg_comm = sum(result["metric_value"] for result in results if result["instances_tested"] > 0) / len(results)
    std_comm = math.sqrt(sum((result["metric_value"] - avg_comm)**2 for result in results if result["instances_tested"] > 0) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={avg_comm} std={std_comm} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")
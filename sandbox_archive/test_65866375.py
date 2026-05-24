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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def quantum_representation(f):
        n = int(math.log2(len(f)))
        Q_f = [[0] * (2**n) for _ in range(2**n)]
        for i in range(2**n):
            for j in range(2**n):
                if f[i] == f[j]:
                    Q_f[i][j] = 1
        return Q_f
    
    def entanglement_matrix(Q_f):
        n = int(math.log2(len(Q_f)))
        M_f = [[0] * (2**n) for _ in range(2**n)]
        for i in range(2**n):
            for j in range(2**n):
                if Q_f[i][j] == 1:
                    M_f[i][j] = 1
        return M_f
    
    def matrix_rank(M):
        n = len(M)
        rank = 0
        for i in range(n):
            if all(x == 0 for x in M[i]):
                continue
            pivot_row = i
            for j in range(i+1, n):
                if abs(M[j][i]) > abs(M[pivot_row][i]):
                    pivot_row = j
            M[i], M[pivot_row] = M[pivot_row], M[i]
            rank += 1
            for j in range(n):
                if j != i:
                    factor = M[j][i] / M[i][i]
                    for k in range(n):
                        M[j][k] -= factor * M[i][k]
        return rank
    
    def BP_ReadTwice_complexity(f):
        n = int(math.log2(len(f)))
        complexity = 0
        for i in range(1, 2**n):
            if f[i] != f[0]:
                complexity += 1
        return complexity
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            f = generate_random_boolean_function(n)
            Q_f = quantum_representation(f)
            M_f = entanglement_matrix(Q_f)
            rank = matrix_rank(M_f)
            size_Q_f = len(Q_f)
            complexity = BP_ReadTwice_complexity(f)
            results.append({
                "n": n,
                "rank": rank,
                "size_Q_f": size_Q_f,
                "complexity": complexity
            })
    
    mean_rank = sum(result["rank"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["rank"] - mean_rank)**2 for result in results) / len(results))
    
    conjecture_holds = all(abs(result["rank"] - mean_rank) <= 3 * std_dev for result in results)
    counterexample = "" if conjecture_holds else "Rank exceeds expected by more than 3 standard deviations"
    
    return {
        "metric_name": "Entanglement Matrix Rank",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_rank)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank exceeds expected by more than 3 standard deviations\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")
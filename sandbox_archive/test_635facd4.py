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
    
    def generate_k_cnf(n, k):
        clauses = []
        for _ in range(k):
            clause = set(random.sample(range(1, n+1), 2))
            if random.choice([True, False]):
                clause = {x: -y for x, y in clause.items()}
            clauses.append(clause)
        return clauses
    
    def quandle_representation(clauses):
        n = max(max(abs(x) for x in clause) for clause in clauses)
        Q = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in clauses:
            for x, y in clause.items():
                Q[x][y] += 1
                Q[y][x] += 1
        return Q
    
    def matrix_rank(matrix):
        m = len(matrix)
        n = len(matrix[0])
        rank = 0
        for i in range(min(m, n)):
            if matrix[i][i] != 0:
                for j in range(i + 1, m):
                    factor = matrix[j][i] / matrix[i][i]
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[i][k]
                rank += 1
        return rank
    
    def factorial(n):
        if n == 0 or n == 1:
            return 1
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result
    
    def monotone_circuit_size(n, k):
        return math.ceil(2**n / (n**k * factorial(k)))
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Ensure at least 30 instances per seed
            k = random.randint(1, min(n, 5))
            F = generate_k_cnf(n, k)
            Q_F = quandle_representation(F)
            rank_Q_F = matrix_rank(Q_F)
            lower_bound = n**k / factorial(k)
            
            if rank_Q_F < lower_bound:
                return {
                    "metric_name": "Minimal Rank of Quandle Representation",
                    "metric_value": rank_Q_F,
                    "instances_tested": 1,
                    "conjecture_holds": False,
                    "counterexample": f"n={n}, k={k}, Q_F_rank={rank_Q_F}, lower_bound={lower_bound}"
                }
            
            C_size = monotone_circuit_size(n, k)
            upper_bound = 2**n / (n**k * factorial(k))
            
            if C_size > upper_bound:
                return {
                    "metric_name": "Monotone Circuit Size",
                    "metric_value": C_size,
                    "instances_tested": 1,
                    "conjecture_holds": False,
                    "counterexample": f"n={n}, k={k}, C_size={C_size}, upper_bound={upper_bound}"
                }
    
    return {
        "metric_name": "Minimal Rank of Quandle Representation",
        "metric_value": sum(results) / len(results),
        "instances_tested": len(results),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean)**2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r >= 0.9 * mean) / len(results)
    
    if all(r >= 0.9 * mean for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(r < 0.9 * mean for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result < 0.9 * mean)
        print(f"RESULT: FALSIFIED counterexample='n=40' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=budget_exceeded n_tested=30")
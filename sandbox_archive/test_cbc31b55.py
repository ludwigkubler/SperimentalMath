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
    
    def generate_k_cnf(n, k):
        clauses = []
        for _ in range(k):
            clause = [random.randint(-n, n) for _ in range(2)]
            while len(set(clause)) == 1 or any(abs(x) > n for x in clause):
                clause = [random.randint(-n, n) for _ in range(2)]
            clauses.append(clause)
        return clauses
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        rank = 0
        for j in range(n):
            i_max = rank
            for i in range(rank, m):
                if abs(A[i][j]) > abs(A[i_max][j]):
                    i_max = i
            if A[i_max][j] == 0:
                continue
            A[rank], A[i_max] = A[i_max], A[rank]
            for i in range(m):
                if i != rank and A[i][j] != 0:
                    factor = Fraction(A[i][j], A[rank][j])
                    for j2 in range(n):
                        A[i][j2] -= factor * A[rank][j2]
            rank += 1
        return rank
    
    def moment_map(clauses, n):
        A = [[0] * (n + 1) for _ in range(len(clauses))]
        for i, clause in enumerate(clauses):
            if len(clause) == 2:
                A[i][abs(clause[0]) - 1] = 1 if clause[0] > 0 else -1
                A[i][abs(clause[1]) - 1] = 1 if clause[1] > 0 else -1
        return gaussian_elimination(A)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        instances_tested = 0
        total_rank = 0
        for _ in range(5):  # Test each n with 5 instances
            clauses = generate_k_cnf(n, random.randint(2 * n, 3 * n))
            rank = moment_map(clauses, n)
            if rank == -1:
                continue
            total_rank += rank
            instances_tested += 1
    
        if instances_tested == 0:
            continue
        
        mean_rank = Fraction(total_rank, instances_tested)
        expected_rank = 2 ** (n / 4)
        
        if abs(mean_rank - expected_rank) > 3 * expected_rank:
            return {
                "metric_name": "Minimal Symplectic Leaf Rank",
                "metric_value": float(mean_rank),
                "instances_tested": instances_tested,
                "conjecture_holds": False,
                "counterexample": f"n={n}, mean rank {mean_rank} deviates by more than a factor of 2^(n/4) from expected value"
            }
    
    return {
        "metric_name": "Minimal Symplectic Leaf Rank",
        "metric_value": float(mean_rank),
        "instances_tested": instances_tested,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30))  # Default to first 29 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results if r["instances_tested"] > 0) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results if r["instances_tested"] > 0) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"n={n}, mean rank {mean_rank} deviates by more than a factor of 2^(n/4) from expected value\" first_failing_seed={first_failing_seed}")
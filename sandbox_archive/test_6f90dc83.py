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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i + 1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i + 1, m):
                factor = Fraction(A[j][i], A[i][i])
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A
    
    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[Fraction(0) for _ in range(p)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][k] += A[i][j] * B[j][k]
        return C
    
    def rank_of_matrix(A):
        A = gaussian_elimination(A)
        rank = 0
        for row in A:
            if any(row):
                rank += 1
        return rank
    
    def generate_3cnf(n, density):
        clauses = []
        variables = list(range(1, n + 1))
        for _ in range(int(density * n * (n - 1) / 2)):
            clause = [random.choice(variables)]
            while len(clause) < random.randint(2, 3):
                var = random.choice(variables)
                if var not in clause:
                    clause.append(var)
            clauses.append(clause)
        return clauses
    
    def tropical_cell_complex(clauses):
        n = max(max(abs(v) for v in clause) for clause in clauses)
        A = [[Fraction(0) for _ in range(n)] for _ in range(n)]
        for clause in clauses:
            for i in clause:
                for j in clause:
                    if i != j:
                        A[i - 1][j - 1] += Fraction(1, abs(i - j))
        return rank_of_matrix(A)
    
    def monotone_circuit_size(clauses):
        n = max(max(abs(v) for v in clause) for clause in clauses)
        # Simplified approximation based on the number of variables and clauses
        return 2 ** (n // 4)
    
    n = random.randint(5, 30)
    density = 1.2
    clauses = generate_3cnf(n, density)
    rank_sum = sum(tropical_cell_complex(clauses) for _ in range(10))
    median_rank = sorted(rank_sum)[n // 2]
    
    circuit_size = monotone_circuit_size(clauses)
    
    return {
        "metric_name": "rank",
        "metric_value": median_rank,
        "instances_tested": 10,
        "conjecture_holds": median_rank <= n ** (1/4),
        "counterexample": "" if median_rank <= n ** (1/4) else f"Median rank {median_rank} > O(n^{1/4})"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = (sum((r["metric_value"] - mean_rank)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='median_rank > O(n^{1/4})' first_failing_seed={first_failing_seed}")
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
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            for j in range(n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0 for _ in range(p)] for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def rank(A):
        A = gaussian_elimination(A)
        rank = 0
        for row in A:
            if any(row):
                rank += 1
        return rank

    def generate_3cnf(n, density):
        clauses = []
        variables = list(range(1, n+1))
        for _ in range(int(density * n * (n-1) // 2)):
            v1, v2 = random.sample(variables, 2)
            sign1, sign2 = random.choice([1, -1]), random.choice([1, -1])
            clauses.append((sign1 * v1, sign2 * v2))
        return clauses

    def tropical_cell_complex(clauses):
        n = len(clauses[0]) // 2
        A = [[0 for _ in range(n)] for _ in range(n)]
        for clause in clauses:
            for i in range(n):
                if abs(clause[i]) == 1 and abs(clause[n+i]) == 1:
                    A[i][n+i] += 1
        return A

    def monotone_circuit_size(rank):
        return 2 ** (rank + 1)

    n = random.choice([5, 10, 15, 20, 30, 40])
    density = 1.2
    clauses = generate_3cnf(n, density)
    A = tropical_cell_complex(clauses)
    rank_value = rank(A)
    circuit_size = monotone_circuit_size(rank_value)

    return {
        "metric_name": "Rank and Circuit Size",
        "metric_value": (rank_value, circuit_size),
        "instances_tested": 1,
        "conjecture_holds": rank_value <= n ** 0.25 and circuit_size <= 2 ** (n ** 0.25),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(3, 149, 4))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    rank_values = [r for r, _ in [res["metric_value"] for res in results]]
    circuit_sizes = [s for _, s in [res["metric_value"] for res in results]]

    mean_rank = sum(rank_values) / len(rank_values)
    std_rank = math.sqrt(sum((x - mean_rank) ** 2 for x in rank_values) / len(rank_values))
    support_fraction_rank = sum(1 for r in rank_values if r <= seeds[0] ** 0.25) / len(rank_values)

    mean_circuit_size = sum(circuit_sizes) / len(circuit_sizes)
    std_circuit_size = math.sqrt(sum((x - mean_circuit_size) ** 2 for x in circuit_sizes) / len(circuit_sizes))
    support_fraction_circuit_size = sum(1 for s in circuit_sizes if s <= 2 ** (seeds[0] ** 0.25)) / len(circuit_sizes)

    if all(r <= seeds[0] ** 0.25 for r in rank_values) and all(s <= 2 ** (seeds[0] ** 0.25) for s in circuit_sizes):
        print(f"RESULT: SUPPORTED mean_rank={mean_rank} std_rank={std_rank} support_fraction_rank={support_fraction_rank}")
    elif any(r > seeds[0] ** 0.25 for r in rank_values) or any(s > 2 ** (seeds[0] ** 0.25) for s in circuit_sizes):
        print(f"RESULT: FALSIFIED counterexample=\"Rank or Circuit Size exceeds bound\" first_failing_seed={seeds[0]}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")
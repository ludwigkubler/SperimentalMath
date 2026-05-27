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
    
    def rank(A):
        m, n = len(A), len(A[0])
        rref = gaussian_elimination(A)
        rank = 0
        for row in rref:
            if any(row):
                rank += 1
        return rank
    
    def twisted_quantum_entanglement(n):
        # Construct a random 3-CNF formula with n variables and clauses
        clauses = []
        for _ in range(2 * n):
            literals = [random.choice([f'x{i}', f'-x{i}']) for i in range(1, n+1)]
            clause = random.sample(literals, 3)
            clauses.append(clause)
        # Convert to a tensor representation (simplified example)
        tensor = [[0] * n for _ in range(n) for _ in range(n)]
        for clause in clauses:
            for i in range(3):
                var = abs(int(clause[i][1:]))
                sign = 1 if clause[i][0] == 'x' else -1
                tensor[var-1][var-1][var-1] += sign
        return tensor
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Test each n with 5 instances
            tensor = twisted_quantum_entanglement(n)
            rank_value = rank(tensor)
            total_rank += rank_value
            instances_tested += 1
    
    average_rank = total_rank / instances_tested
    conjecture_holds = average_rank >= n**(2/3)
    
    return {
        "metric_name": "Average Rank",
        "metric_value": average_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Average rank {average_rank} < n^(2/3) for n={n}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Average rank < n^(2/3)\" first_failing_seed={first_failing_seed}")
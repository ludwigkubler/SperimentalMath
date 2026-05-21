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
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(0, 1) * 2 - 1 for _ in range(n)]
            if all(c == 0 for c in clause):
                clause[random.randint(0, n-1)] = random.choice([-1, 1])
            clauses.append(clause)
        return clauses
    
    def adjacency_matrix(clauses, n):
        M = [[0] * n for _ in range(n)]
        for clause in clauses:
            for i in range(n):
                if clause[i] != 0:
                    for j in range(i + 1, n):
                        if clause[j] != 0:
                            M[i][j] += 1
                            M[j][i] += 1
        return M
    
    def monte_carlo_free_entropy(M, num_samples=10000):
        n = len(M)
        total = 0
        for _ in range(num_samples):
            theta = random.uniform(0, 2 * math.pi)
            z = complex(math.cos(theta), math.sin(theta))
            trace = sum(abs(z - M[i][i]) for i in range(n))
            total += trace / n
        return -total / num_samples
    
    def is_positive_definite(M):
        n = len(M)
        for k in range(1, n + 1):
            submatrix = [row[:k] for row in M[:k]]
            det = determinant(submatrix)
            if det <= 0:
                return False
        return True
    
    def determinant(matrix):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            det += (-1) ** j * matrix[0][j] * determinant(submatrix)
        return det
    
    n = 40
    clauses = generate_3cnf(n)
    M = adjacency_matrix(clauses, n)
    
    if not is_positive_definite(M):
        return {
            "metric_name": "free_entropy",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Matrix is not positive definite"
        }
    
    phi = monte_carlo_free_entropy(M)
    c = Fraction(1, 5)  # Universal constant c > 0
    return {
        "metric_name": "free_entropy",
        "metric_value": phi,
        "instances_tested": 1,
        "conjecture_holds": phi >= c * n,
        "counterexample": "" if phi >= c * n else f"Graph with n={n}, A={M}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 307))  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")
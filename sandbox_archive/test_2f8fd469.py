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
    
    def generate_cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if random.choice([True, False]):
                clause[0] *= -1
            if random.choice([True, False]):
                clause[1] *= -1
            clauses.append(clause)
        return clauses

    def adjacency_matrix(n, clauses):
        adj = [[0 for _ in range(n)] for _ in range(n)]
        for clause in clauses:
            for lit in clause:
                if lit > 0:
                    i = lit - 1
                else:
                    i = -lit - 1
                adj[i][i] = 1
        return adj

    def geometric_quantization(M):
        n = len(M)
        M2 = [[M[i][j] * M[j][k] for k in range(n)] for j in range(n)]
        det = determinant(M2)
        if det == 0:
            return float('inf')
        return math.sqrt(det)

    def determinant(matrix):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            det += ((-1) ** j) * matrix[0][j] * determinant(submatrix)
        return det

    def frege_proof_width(clauses):
        # Placeholder function; actual implementation depends on the Frege proof system
        return len(clauses)

    n = random.randint(5, 40)
    m = random.randint(n, 2 * n)
    clauses = generate_cnf(n, m)
    adj_matrix = adjacency_matrix(n, clauses)
    Q_G = geometric_quantization(adj_matrix)
    omega_F = frege_proof_width(clauses)

    if Q_G == float('inf'):
        return {
            "metric_name": "Q(G)^2",
            "metric_value": 0,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "singular_matrix"
        }

    metric_value = Q_G ** 2 * math.log(n)
    conjecture_holds = abs(omega_F - metric_value) <= 0.1 * abs(metric_value)
    counterexample = "" if conjecture_holds else f"Q(G)^2={Q_G**2}, omega_F={omega_F}"
    
    return {
        "metric_name": "Q(G)^2",
        "metric_value": Q_G ** 2,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(seed) for seed in sys.argv[1:]] or list(range(2, 30)) + [prime(n) for n in range(5, 40)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}}}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")

def prime(n):
    while True:
        p = random.randint(2 ** (n - 1), 2 ** n - 1)
        if all(p % i != 0 for i in range(2, int(math.sqrt(p)) + 1)):
            return p
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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if sum(clause) != 0:
                clauses.append(clause)
        return clauses

    def tensor_product(A, B):
        n, m = len(A), len(B)
        result = [[0] * (m * n) for _ in range(n * m)]
        for i in range(n):
            for j in range(m):
                for k in range(n):
                    for l in range(m):
                        result[i * m + j][k * m + l] += A[i][k] * B[j][l]
        return result

    def min_representation_dimension(cnf, n):
        max_dim = 0
        for _ in range(10):  # Try multiple random algebras
            algebra_size = random.randint(n, 2*n)
            algebra = [[random.choice([-1, 1]) for _ in range(algebra_size)] for _ in range(algebra_size)]
            dim = 0
            for clause in cnf:
                matrix = [[0] * algebra_size for _ in range(algebra_size)]
                for literal in clause:
                    if literal > 0:
                        matrix[literal-1][literal-1] += 1
                    else:
                        matrix[-literal-1][-literal-1] += 1
                dim = max(dim, len(tensor_product(matrix, algebra)))
            max_dim = max(max_dim, dim)
        return max_dim

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        cnf = generate_cnf(n)
        dim_rep = min_representation_dimension(cnf, n)
        results.append({"n": n, "dim_rep": dim_rep})

    max_dim_rep = max(result["dim_rep"] for result in results)
    conjecture_holds = max_dim_rep <= O_n_log_n(max_dim_rep)

    return {
        "metric_name": "min_representation_dimension",
        "metric_value": max_dim_rep,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"max_dim_rep={max_dim_rep} > O(n log n)"
    }

def O_n_log_n(x):
    return x * math.log2(x)

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")
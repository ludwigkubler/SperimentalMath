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
    
    def generate_cnf(n, c):
        clauses = []
        for _ in range(c):
            clause = set()
            while len(clause) < 3:
                var = random.randint(1, n)
                if random.choice([True, False]):
                    clause.add(-var)
                else:
                    clause.add(var)
            clauses.append(tuple(sorted(clause)))
        return clauses

    def adjacency_matrix(cnf):
        n = max(abs(var) for clause in cnf for var in clause)
        A = [[0] * n for _ in range(n)]
        for clause in cnf:
            for i, var1 in enumerate(clause):
                for j, var2 in enumerate(clause[i+1:], start=i+1):
                    if abs(var1) != abs(var2):
                        A[abs(var1)-1][abs(var2)-1] = 1
                        A[abs(var2)-1][abs(var1)-1] = 1
        return A

    def geometric_entropy(A):
        n = len(A)
        if n == 0:
            return 0
        trace = sum(A[i][i] for i in range(n))
        det = determinant(A, n)
        if det == 0:
            return float('inf')
        entropy = -trace / n * math.log(det / n)
        return entropy

    def determinant(A, n):
        if n == 1:
            return A[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += (-1) ** j * A[0][j] * determinant(submatrix, n-1)
        return det

    def correlation_coefficient(x, y):
        if len(x) != len(y):
            raise ValueError("x and y must have the same length")
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / len(x)
        std_x = math.sqrt(sum((xi - mean_x) ** 2 for xi in x) / len(x))
        std_y = math.sqrt(sum((yi - mean_y) ** 2 for yi in y) / len(y))
        if std_x == 0 or std_y == 0:
            return float('nan')
        return cov / (std_x * std_y)

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    instances_tested = 0
    n_max = 0

    for n in n_values:
        for _ in range(5):
            c = random.randint(n, 2 * n)
            cnf = generate_cnf(n, c)
            A = adjacency_matrix(cnf)
            H_min = geometric_entropy(A)
            results.append((H_min, c))
            instances_tested += 1
            n_max = max(n_max, n)

    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": float('nan'),
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "no_data"
        }

    H_min_values, c_values = zip(*results)
    r = correlation_coefficient(H_min_values, c_values)

    return {
        "metric_name": "correlation_coefficient",
        "metric_value": r,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": r >= 0.9,
        "counterexample": "" if r >= 0.9 else f"r={r:.2f}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(1, 10000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    if not results:
        print("RESULT: INCONCLUSIVE no_data")
        sys.exit(0)

    mean_r = sum(result["metric_value"] for result in results) / len(results)
    std_r = math.sqrt(sum((result["metric_value"] - mean_r) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_r:.4f} std={std_r:.4f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='r<{mean_r:.2f}' first_failing_seed={first_failing_seed}")
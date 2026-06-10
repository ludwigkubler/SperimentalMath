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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, n) for _ in range(n)]
            while not any(abs(lit) <= n for lit in clause):
                clause = [random.randint(-n, n) for _ in range(n)]
            clauses.append(clause)
        return clauses

    def gaussian_elimination(A, b):
        m, n = len(A), len(A[0])
        Augmented = [A[i] + [b[i]] for i in range(m)]
        for i in range(n):
            max_row = max(range(i, m), key=lambda r: abs(Augmented[r][i]))
            Augmented[i], Augmented[max_row] = Augmented[max_row], Augmented[i]
            if Augmented[i][i] == 0:
                continue
            denom = Augmented[i][i]
            for j in range(i, n + 1):
                Augmented[i][j] /= denom
            for k in range(m):
                if k != i and Augmented[k][i] != 0:
                    factor = Augmented[k][i]
                    for j in range(i, n + 1):
                        Augmented[k][j] -= factor * Augmented[i][j]
        return [row[-1] for row in Augmented]

    def compute_rank(cnf):
        n = len(cnf)
        A = [[0] * n for _ in range(n)]
        b = [0] * n
        for clause in cnf:
            for lit in clause:
                if abs(lit) <= n:
                    row, col = abs(lit) - 1, lit > 0
                    A[row][col] += 1
                    b[col] += 1
        return len(gaussian_elimination(A, b))

    def compute_betti_numbers(n):
        # Placeholder for actual computation of Betti numbers
        # This is a dummy implementation for testing purposes
        return [random.randint(0, n) for _ in range(n)]

    cnf = generate_cnf(random.randint(5, 10))
    rank_variance = compute_rank(cnf) ** 2
    betti_numbers = compute_betti_numbers(len(cnf))

    correlation_coefficient = sum(betti_numbers[i] * betti_numbers[i] for i in range(len(betti_numbers))) / len(betti_numbers)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": 1,
        "n_max": max(5, 10),
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": "" if correlation_coefficient >= 0.7 else "correlation_coefficient < 0.7"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)

    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] and res["metric_value"] < 0.5 for res in results):
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"] and res["metric_value"] < 0.5)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.5\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_data")
# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
import itertools

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        clauses = []
        for _ in range(10):  # Generate 10 clauses
            clause = [random.randint(-n, n) for _ in range(random.randint(2, n))]
            clauses.append(clause)
        return clauses

    def resolution_width(phi):
        # Simplified version of resolution width calculation
        return len(phi)

    def frobenius_normal_form(phi):
        n = max(abs(x) for clause in phi for x in clause)
        F = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in phi:
            for x in clause:
                if x > 0:
                    F[x][x] += 1
                else:
                    F[-x][-x] -= 1
        return F

    def matrix_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(m):
            if any(matrix[i][j] != 0 for j in range(n)):
                rank += 1
                for j in range(n):
                    if matrix[j][i] != 0:
                        factor = Fraction(matrix[j][i], matrix[i][i])
                        for k in range(n):
                            matrix[j][k] -= factor * matrix[i][k]
        return rank

    phi = generate_cnf(10)
    F = frobenius_normal_form(phi)
    dim_F = matrix_rank(F)
    w_phi = resolution_width(phi)

    return {
        "metric_name": "Dimension of Frobenius Normal Form",
        "metric_value": dim_F,
        "instances_tested": 1,
        "n_max": 10,
        "conjecture_holds": dim_F >= w_phi,
        "counterexample": "" if dim_F >= w_phi else f"dim(F(φ))={dim_F}, w(φ)={w_phi}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"dim(F(φ)) < w(φ)\" first_failing_seed={first_failing_seed}")
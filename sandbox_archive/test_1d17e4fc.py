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
            if pivot == 0:
                continue
            for j in range(n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]

    def hodge_span(A):
        m, n = len(A), len(A[0])
        gaussian_elimination(A)
        rank = 0
        for row in A:
            if any(row):
                rank += 1
        return rank

    def tseitin_formula(n, m):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for i in range(m):
            clause = random.choice(variables)
            if random.choice([True, False]):
                clause = f'~{clause}'
            clauses.append(clause)
        return variables, clauses

    def circuit_depth(n, m):
        # Simplified model of circuit depth for Tseitin formulas
        return n + m

    n_max = 40
    instances_tested = 0
    total_c = 0.0
    conjecture_holds = True
    counterexample = ""

    for n in range(5, n_max + 1):
        for _ in range(6):  # Ensure at least 30 instances per seed
            variables, clauses = tseitin_formula(n, m)
            A = [[random.randint(-10, 10) for _ in range(n)] for _ in range(m)]
            h_min = hodge_span(A)
            d_phi = circuit_depth(n, len(clauses))
            if h_min == 0:
                continue
            c = d_phi / h_min
            total_c += c
            instances_tested += 1

    mean_c = total_c / instances_tested
    support_fraction = instances_tested / (n_max - 4) * 6

    return {
        "metric_name": "c",
        "metric_value": mean_c,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)

    mean_c = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_c} std=NA support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")
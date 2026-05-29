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
            max_row = i + max(range(i, m), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(n):
                if j != i:
                    factor = A[j][i] / A[i][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def determinant(A):
        m, n = len(A), len(A[0])
        if m != n:
            raise ValueError("Matrix must be square")
        if n == 1:
            return A[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += (-1) ** j * A[0][j] * determinant(submatrix)
        return det

    def hodge_span(A):
        m, n = len(A), len(A[0])
        rank = 0
        for i in range(m):
            if all(abs(A[i][j]) < 1e-9 for j in range(n)):
                continue
            pivot_col = next(j for j in range(n) if abs(A[i][j]) > 1e-9)
            A[i] /= A[i][pivot_col]
            for j in range(m):
                if j != i:
                    factor = A[j][pivot_col]
                    A[j] -= factor * A[i]
            rank += 1
        return rank

    def tseitin_formula(n, m):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(m):
            clause = [random.choice(variables) if random.randint(0, 1) else -random.choice(variables) for _ in range(random.randint(2, n))]
            clauses.append(clause)
        return variables, clauses

    def circuit_depth(clauses):
        depth = 0
        for clause in clauses:
            depth = max(depth, len(clause))
        return depth

    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            variables, clauses = tseitin_formula(n, m=2 * n)
            A = [[0] * (n + 1) for _ in range(n + 1)]
            for var in variables:
                A[var - 1][var - 1] = 1
            for clause in clauses:
                for lit in clause:
                    if lit > 0:
                        A[lit - 1][0] += 1
                    else:
                        A[-lit - 1][0] -= 1
            h_min = hodge_span(A)
            d_phi = circuit_depth(clauses)
            results.append((h_min, d_phi))

    if not results:
        return {
            "metric_name": "c",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    h_mins, d_phis = zip(*results)
    c_values = [d_phi / h_min for h_min, d_phi in zip(h_mins, d_phis)]
    c_mean = sum(c_values) / len(c_values)

    return {
        "metric_name": "c",
        "metric_value": c_mean,
        "instances_tested": len(results),
        "n_max": max([5, 10, 15, 20, 30, 40]),
        "conjecture_holds": all(c <= 1 for c in c_values),
        "counterexample": "" if all(c <= 1 for c in c_values) else "c > 1"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_c = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = sum(1 for r in results if "conjecture_holds" in r and r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_c} std=0 support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] != "" for r in results):
        first_failing_seed = next(r["seed"] for r in results if "counterexample" in r and r["counterexample"] != "")
        print(f"RESULT: FALSIFIED counterexample=\"{next(r['counterexample'] for r in results if 'counterexample' in r)}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")
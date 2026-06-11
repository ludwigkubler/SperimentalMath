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
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                continue
            factor = 1 / A[i][i]
            for j in range(n):
                A[i][j] *= factor
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def dpll(cnf, assignment=[]):
        if not cnf:
            return True
        literal = next((l for l in cnf[0] if l > 0), None)
        if literal is None:
            return False
        assignment.append(literal)
        new_cnf = [c for c in cnf if literal not in c and -literal not in c]
        if dpll(new_cnf, assignment):
            return True
        assignment.pop()
        assignment.append(-literal)
        new_cnf = [c for c in cnf if -literal not in c and literal not in c]
        if dpll(new_cnf, assignment):
            return True
        assignment.pop()
        return False

    def hodge_mumford_cohomology(cnf):
        n = len(cnf)
        A = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(1, n + 1):
            A[i][i - 1] = 1
            A[i][i] = -1
        B = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in cnf:
            for literal in clause:
                if literal > 0:
                    B[literal - 1][literal - 1] += 1
                else:
                    B[-literal - 1][-literal - 1] -= 1
        C = matrix_multiplication(A, B)
        C = gaussian_elimination(C)
        rank = sum(1 for row in C if any(x != 0 for x in row))
        return rank

    random.seed(seed)
    n = random.randint(5, 40)
    cnf = []
    for _ in range(random.randint(2 * n, 3 * n)):
        clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
        if all(lit not in clause and -lit not in clause for lit in cnf):
            cnf.append(clause)
    h_values = []
    w_dpll_values = []
    for _ in range(30):
        assignment = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
        if dpll(cnf, assignment):
            h_value = hodge_mumford_cohomology(cnf)
            w_dpll_value = len(dpll(cnf))
            h_values.append(h_value)
            w_dpll_values.append(w_dpll_value)

    correlation_coefficient = sum((h - mean_h) * (w - mean_w) for h, w in zip(h_values, w_dpll_values)) / (len(h_values) * std_h * std_w)
    max_ratio = max(abs(h / w) for h, w in zip(h_values, w_dpll_values))

    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(h_values),
        "n_max": n,
        "conjecture_holds": correlation_coefficient >= 0.7 and max_ratio <= 2,
        "counterexample": "" if correlation_coefficient >= 0.7 and max_ratio <= 2 else f"correlation_coefficient={correlation_coefficient}, max_ratio={max_ratio}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(1, 97) for _ in range(30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)

    mean_h = sum(r["metric_value"] for r in results) / len(results)
    std_h = math.sqrt(sum((r["metric_value"] - mean_h) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_h} std={std_h} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")
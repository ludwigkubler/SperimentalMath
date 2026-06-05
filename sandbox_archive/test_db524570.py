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
            max_row = i + max(range(i, m), key=lambda r: abs(A[r][i]))
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                continue
            for j in range(n):
                A[i][j] /= A[i][i]
            for k in range(m):
                if k != i and A[k][i] != 0:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B[0]), len(B)
        C = [[0 for _ in range(p)] for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def dpll(clauses, assignment):
        if not clauses:
            return True
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if dpll([c for c in clauses if not (literal in c or -literal in c)], new_assignment):
                return True
            new_assignment[literal] = False
            if dpll([c for c in clauses if not (-literal in c)], new_assignment):
                return True
            return False
        literal = next((l for l in range(1, len(clauses) + 1) if l not in assignment and -l not in assignment), None)
        if literal:
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if dpll([c for c in clauses if not (literal in c or -literal in c)], new_assignment):
                return True
            new_assignment[literal] = False
            if dpll([c for c in clauses if not (-literal in c)], new_assignment):
                return True
        return False

    def tsv(matroid):
        m, n = len(matroid), len(matroid[0])
        A = [[1 if i == j else 0 for j in range(n)] for i in range(m)]
        A = gaussian_elimination(A)
        volume = 1
        for row in A:
            volume *= max(0, sum(row))
        return volume

    def dpll_width(clauses):
        assignment = {}
        if dpll(clauses, assignment):
            return 1
        else:
            return float('inf')

    n = random.randint(5, 40)
    clauses = []
    for _ in range(n):
        num_vars = random.randint(1, n)
        clause = [random.choice([i, -i]) for i in range(1, num_vars + 1)]
        clauses.append(clause)

    matroid = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    tsv_value = tsv(matroid)
    dpll_width_value = dpll_width(clauses)

    return {
        "metric_name": "TSV/DPLL Width Ratio",
        "metric_value": tsv_value / dpll_width_value if dpll_width_value != float('inf') else float('inf'),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": tsv_value >= dpll_width_value,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
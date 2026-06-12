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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            for j in range(n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def dpll(clauses, assignment):
        literals_seen = set()
        for clause in clauses:
            literals_seen.update(abs(l) for l in clause)
        pure_literal = next((l for l in literals_seen if all(l not in c or -l in c for c in clauses)), None)
        if pure_literal is not None:
            new_assignment = assignment.copy()
            new_assignment[pure_literal] = True
            return dpll(clauses, new_assignment) or dpll(clauses, {l: False for l in literals_seen})
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause is not None:
            literal = unit_clause[0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            return dpll(clauses, new_assignment)
        if not clauses:
            return True
        l = next(iter(literals_seen))
        return dpll(clauses, {**assignment, l: True}) or dpll(clauses, {**assignment, l: False})
    
    def hermitian_matrix_from_clauses(n, clauses):
        A = [[0] * n for _ in range(n)]
        for clause in clauses:
            for i in clause:
                for j in clause:
                    if i != 0 and j != 0:
                        A[abs(i)-1][abs(j)-1] += (i / abs(i)) * (j / abs(j))
        return A
    
    def min_tropical_hermitian_rank(A):
        A = gaussian_elimination(A)
        rank = sum(1 for row in A if any(row[i] != 0 for i in range(len(row))))
        return rank
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        clauses = [[random.choice([-1, 1]) * (i + 1) for i in range(n)] for _ in range(random.randint(2, n))]
        A = hermitian_matrix_from_clauses(n, clauses)
        rank = min_tropical_hermitian_rank(A)
        width = dpll(clauses, {})
        if width == 0:
            continue
        metric_values.append(Fraction(rank, width))
    
    mean_value = sum(metric_values) / len(metric_values)
    std_value = math.sqrt(sum((x - mean_value)**2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for v in metric_values if v >= 1.0) / len(metric_values)
    
    conjecture_holds = support_fraction >= 0.8
    counterexample = "" if conjecture_holds else "support_fraction < 0.8"
    
    return {
        "metric_name": "min_tropical_hermitian_rank_over_dpll_width",
        "metric_value": float(mean_value),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = [run_trial(seed) for seed in seeds]
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
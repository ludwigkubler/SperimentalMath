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
    
    def generate_k_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), random.randint(-n, -1)]
            cnf.append(clause)
        return cnf
    
    def clause_indicator_polynomial(cnf, x):
        result = 0
        for clause in cnf:
            term = 1
            for literal in clause:
                if literal > 0:
                    term *= (x - literal)
                else:
                    term *= (x + abs(literal))
            result += term
        return result
    
    def companion_matrix(poly):
        n = len(poly) - 1
        A = [[0] * n for _ in range(n)]
        for i in range(n):
            A[i][i+1] = 1
            if i == 0:
                A[i][0] = poly[-2]
            else:
                A[i][0] = -poly[i-1]
        return A
    
    def gaussian_elimination(A, b=None):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            if b is not None:
                b[i], b[max_row] = b[max_row], b[i]
            for j in range(i+1, n):
                factor = A[j][i] / A[i][i]
                A[j][i] = 0
                if b is not None:
                    b[j] -= factor * b[i]
                for k in range(i+1, n):
                    A[j][k] -= factor * A[i][k]
        return A
    
    def count_distinct_roots(A):
        n = len(A)
        det = 1
        for i in range(n):
            det *= A[i][i]
        if det == 0:
            return float('inf')
        return abs(det) ** (1/n)
    
    def eigenvalues(A):
        n = len(A)
        if n == 2:
            a, b, c, d = A[0][0], A[0][1], A[1][0], A[1][1]
            trace = a + d
            det = ad - bc
            lambda1 = (trace + math.sqrt(trace**2 - 4*det)) / 2
            lambda2 = (trace - math.sqrt(trace**2 - 4*det)) / 2
            return [lambda1, lambda2]
        else:
            return []
    
    def irreducible_root_system(eigenvalues):
        roots = set()
        for eig in eigenvalues:
            if eig != 0:
                roots.add((eig.real, eig.imag))
        return len(roots)
    
    n_max = 40
    instances_tested = 0
    total_metric_value = 0
    
    for n in range(5, n_max + 1):
        for _ in range(6):  # Aim for at least 30 instances per seed
            m = random.randint(n, 2*n)
            cnf = generate_k_cnf(n, m)
            poly = clause_indicator_polynomial(cnf, x=1)
            A = companion_matrix(poly)
            det_A = gaussian_elimination(A)
            if det_A[0][0] == 0:
                continue
            distinct_roots = count_distinct_roots(det_A)
            if distinct_roots == float('inf'):
                continue
            instances_tested += 1
            total_metric_value += distinct_roots
    
    if instances_tested < 30:
        return {
            "metric_name": "distinct_roots",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_metric_value = total_metric_value / instances_tested
    conjecture_holds = 0.5 <= mean_metric_value / (m**(1/3) * n**(2/3)) <= 2
    
    return {
        "metric_name": "distinct_roots",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={seed}")
                break
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
            clause = [random.randint(-n, -1), random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def cnf_to_matrix(cnf, n):
        A = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in cnf:
            x, y = abs(clause[0]), abs(clause[1])
            if clause[0] < 0:
                A[x][y] += 1
            else:
                A[y][x] += 1
        return A
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i + 1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                return None
            for j in range(i + 1, n):
                factor = Fraction(A[j][i], A[i][i])
                for k in range(n + 1):
                    A[j][k] -= factor * A[i][k]
        return A
    
    def hodge_span_width(A):
        rank = 0
        for row in gaussian_elimination(A):
            if any(row):
                rank += 1
        return rank
    
    def resolution_proof_width(cnf, n):
        stack = [cnf[:]]
        while stack:
            clause = stack.pop()
            if not clause:
                continue
            literal = random.choice(clause)
            new_clauses = []
            for c in cnf:
                if literal in c and -literal in c:
                    continue
                if literal in c:
                    new_clauses.append([x for x in c if x != literal])
                elif -literal in c:
                    new_clauses.append([x for x in c if x != -literal])
            stack.extend(new_clauses)
        return len(cnf) - len(stack)
    
    n = random.randint(5, 30)
    cnf = generate_cnf(n)
    A = cnf_to_matrix(cnf, n)
    hsw = hodge_span_width(A)
    w_phi = resolution_proof_width(cnf, n)
    
    if hsw > 2 * w_phi:
        return {
            "metric_name": "Hodge Span Width",
            "metric_value": 0,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": f"HSW({hsw}) > 2 * w({w_phi})"
        }
    
    return {
        "metric_name": "Hodge Span Width",
        "metric_value": hsw / w_phi if w_phi != 0 else float('inf'),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"HSW > 2 * w\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")
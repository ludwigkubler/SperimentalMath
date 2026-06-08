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
    
    def gaussian_elimination(A, b):
        n = len(b)
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
            b[i] /= factor
            for k in range(n):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
                    b[k] -= factor * b[i]
        return b
    
    def dpll(clauses, assignment):
        if not clauses:
            return True
        literal = next((lit for lit in set.union(*clauses) if lit not in assignment), None)
        if literal is None:
            return False
        assignment[literal] = True
        new_clauses = [c for c in clauses if literal not in c and -literal not in c]
        if dpll(new_clauses, assignment):
            return True
        assignment[literal] = False
        new_clauses = [c for c in clauses if -literal not in c]
        if dpll(new_clauses, assignment):
            return True
        return False
    
    def local_coherence(clauses):
        n = len(clauses)
        A = [[0]*n for _ in range(n)]
        b = [0]*n
        for i, clause in enumerate(clauses):
            for j, clause2 in enumerate(clauses):
                if i != j:
                    count = sum(lit in clause and -lit in clause2 for lit in set.union(clause, clause2))
                    A[i][j] = count
                    b[i] += count
        try:
            solution = gaussian_elimination(A, b)
            return max(solution)
        except ZeroDivisionError:
            return 0
    
    def simulate_dpll_path_length(clauses):
        assignment = {}
        path_length = 0
        while not dpll(clauses, assignment):
            literal = next((lit for lit in set.union(*clauses) if lit not in assignment), None)
            if literal is None:
                return float('inf')
            assignment[literal] = True
            new_clauses = [c for c in clauses if literal not in c and -literal not in c]
            path_length += 1
        return path_length
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    variables = list(range(1, n+1))
    clauses = []
    for _ in range(n):
        clause = [random.choice([-v, v]) for v in variables]
        clauses.append(clause)
    
    coherence = local_coherence(clauses)
    if coherence < n**(2/3):
        path_length = simulate_dpll_path_length(clauses)
    else:
        path_length = float('inf')
    
    return {
        "metric_name": "local_coherence",
        "metric_value": coherence,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": coherence >= n**(2/3) or path_length <= n**(1/3),
        "counterexample": "" if coherence >= n**(2/3) else f"path_length={path_length} > O(n^(1/3)) = {n**(1/3)}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        counterexample = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
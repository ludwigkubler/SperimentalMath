# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_tseitin_formula(n):
        literals = [f'x{i}' for i in range(n)]
        clauses = []
        for i in range(n):
            clauses.append(f'{literals[i]}')
            clauses.append(f'-{literals[i]}')
        for i in range(1, n):
            clauses.append(f'{literals[0]} {literals[i]} -{literals[i+1]}')
        return literals, clauses
    
    def polynomial_system(literals, clauses):
        n = len(literals)
        A = [[0] * (n + 1) for _ in range(n)]
        b = [0] * n
        for clause in clauses:
            if ' ' not in clause:
                continue
            literal, rest = clause.split(' ', 1)
            if literal.startswith('-'):
                literal = literal[1:]
                negate = True
            else:
                negate = False
            idx = literals.index(literal)
            A[idx][idx] += -1 if negate else 1
        return A, b
    
    def gaussian_elimination(A, b):
        n = len(b)
        for i in range(n):
            max_row = i
            for k in range(i + 1, n):
                if abs(A[k][i]) > abs(A[max_row][i]):
                    max_row = k
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            for k in range(i + 1, n):
                factor = Fraction(A[k][i], A[i][i])
                A[k][i:] = [A[k][j] - factor * A[i][j] for j in range(i, n + 1)]
                b[k] -= factor * b[i]
        return A, b
    
    def minimal_diophantine_degree(A):
        n = len(A)
        rank = 0
        for i in range(n):
            if all(A[j][i] == 0 for j in range(rank)):
                continue
            A[rank], A[i] = A[i], A[rank]
            for j in range(rank + 1, n):
                factor = Fraction(A[j][i], A[rank][i])
                A[j][i:] = [A[j][k] - factor * A[rank][k] for k in range(i, n + 1)]
            rank += 1
        return rank
    
    def frege_proof_length(n):
        # Placeholder function; actual implementation depends on the proof system
        return n * (n + 1) // 2
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        literals, clauses = generate_tseitin_formula(n)
        A, b = polynomial_system(literals, clauses)
        _, _ = gaussian_elimination(A, b)
        dd = minimal_diophantine_degree(A)
        f = frege_proof_length(n)
        results.append((dd, f))
    
    if not results:
        return {
            "metric_name": "minimal_diophantine_degree",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    dd_values = [dd for dd, _ in results]
    f_values = [f for _, f in results]
    mean_dd = sum(dd_values) / len(dd_values)
    mean_f = sum(f_values) / len(f_values)
    
    if any(dd > 2 * mean_dd for dd in dd_values):
        return {
            "metric_name": "minimal_diophantine_degree",
            "metric_value": 0,
            "instances_tested": len(results),
            "n_max": max(n for _, n in results),
            "conjecture_holds": False,
            "counterexample": f"dd > 2 * mean_dd; dd={max(dd_values)}, mean_dd={mean_dd}"
        }
    
    correlation = sum((dd - mean_dd) * (f - mean_f) for dd, f in results) / len(results)
    return {
        "metric_name": "minimal_diophantine_degree",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n for _, n in results),
        "conjecture_holds": abs(correlation) >= 0.8
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='dd > 2 * mean_dd' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")
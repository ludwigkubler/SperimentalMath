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
    
    def generate_sat_instance(n):
        variables = set()
        clauses = []
        for _ in range(2 * n):
            clause = [random.choice([f'x{i}', f'-x{i}']) for i in range(1, n + 1)]
            clauses.append(clause)
            variables.update(clause)
        return list(variables), clauses
    
    def incidence_algebra(clauses):
        n = len(set(var[2:] for var in sum(clauses, [])))
        A = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in clauses:
            for literal in clause:
                if literal.startswith('x'):
                    i = int(literal[1:]) - 1
                else:
                    i = int(literal[2:]) - 1
                A[i][i] += 1
        return A
    
    def matrix_rank(A):
        m, n = len(A), len(A[0])
        rank = 0
        for col in range(n):
            pivot_row = None
            for row in range(rank, m):
                if A[row][col] != 0:
                    pivot_row = row
                    break
            if pivot_row is not None:
                A[pivot_row], A[rank] = A[rank], A[pivot_row]
                rank += 1
                for row in range(m):
                    if row != rank - 1:
                        factor = A[row][col] / A[rank - 1][col]
                        for j in range(n):
                            A[row][j] -= factor * A[rank - 1][j]
        return rank
    
    def local_system_order(A):
        rank = matrix_rank(A)
        n = len(A) - 1
        if rank != n:
            raise ValueError("Matrix is singular")
        order = Fraction(1, math.factorial(n))
        for i in range(n + 1):
            for j in range(i + 1, n + 1):
                order *= Fraction(A[i][j], A[j][i])
        return order
    
    def resolution_length(clauses):
        stack = []
        for clause in clauses:
            if not any(literal in stack for literal in clause):
                stack.append(random.choice(clause))
        length = len(stack)
        while stack:
            literal = stack.pop()
            new_clauses = [c for c in clauses if literal not in c and '-x' + literal not in c]
            if not new_clauses:
                break
            stack.extend(new_clause for clause in new_clauses if literal not in clause and '-x' + literal not in clause)
            length += len(stack)
        return length
    
    variables, clauses = generate_sat_instance(40)
    A = incidence_algebra(clauses)
    try:
        OInc_phi = local_system_order(A)
    except ValueError as e:
        return {
            "metric_name": "Local System Order",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": 40,
            "conjecture_holds": False,
            "counterexample": str(e)
        }
    
    L_phi = resolution_length(clauses)
    
    return {
        "metric_name": "Resolution Proof Length",
        "metric_value": L_phi,
        "instances_tested": 1,
        "n_max": 40,
        "conjecture_holds": L_phi >= OInc_phi / 2,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(result["conjecture_holds"] for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Resolution proof length less than half local system order\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")
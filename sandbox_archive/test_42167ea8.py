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
        variables = list(range(1, n+1))
        clauses = []
        for _ in range(n):
            clause = random.sample(variables, 2)
            clauses.append(clause)
        return clauses
    
    def incidence_algebra(clauses):
        n = len(clauses)
        A = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(1, n + 1):
            for j in range(i, n + 1):
                if any(set(clause).issubset({i, j}) for clause in clauses):
                    A[i][j] = 1
        return A
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        rank = 0
        for i in range(n):
            max_row = None
            for j in range(rank, m):
                if A[j][i]:
                    max_row = j
                    break
            if max_row is None:
                continue
            A[max_row], A[rank] = A[rank], A[max_row]
            for j in range(n):
                if j != i and A[rank][j]:
                    factor = Fraction(A[j][i], A[rank][i])
                    for k in range(n + 1):
                        A[j][k] -= factor * A[rank][k]
            rank += 1
        return rank
    
    def local_system_order(A):
        m, n = len(A), len(A[0])
        if m != n:
            raise ValueError("Matrix is not square")
        order = gaussian_elimination(A)
        return order
    
    def resolution_proof_length(clauses):
        n = len(clauses)
        clauses = [sorted(clause) for clause in clauses]
        clauses.sort(key=len)
        stack = []
        for clause in clauses:
            if all(x not in stack for x in clause):
                stack.extend(clause)
            else:
                return 1
        return len(stack)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        total_length = 0
        total_order = 0
        
        while instances_tested < 30:
            clauses = generate_sat_instance(n)
            try:
                A = incidence_algebra(clauses)
                order = local_system_order(A)
                length = resolution_proof_length(clauses)
                
                if length >= order / 2:
                    results.append((n, length, order))
                    instances_tested += 1
                    total_length += length
                    total_order += order
            except (ValueError, ZeroDivisionError):
                continue
        
        if not results:
            return {
                "metric_name": "Resolution Proof Length vs Local System Order",
                "metric_value": None,
                "instances_tested": 0,
                "n_max": n_values[-1],
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
    
    mean_length = total_length / len(results)
    mean_order = total_order / len(results)
    correlation_coefficient = sum((x[1] - mean_length) * (x[2] - mean_order) for x in results) / len(results)
    
    return {
        "metric_name": "Resolution Proof Length vs Local System Order",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": n_values[-1],
        "conjecture_holds": correlation_coefficient >= 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(x["metric_value"] for x in results if x["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((x["metric_value"] - mean_metric_value) ** 2 for x in results if x["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for x in results if x["conjecture_holds"]) / len(results)
    
    if all(x["metric_value"] is not None for x in results):
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
        else:
            first_failing_seed = next(i for i, x in enumerate(results) if not x["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample='correlation_coefficient<0.5' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE some trials had None metric_value")
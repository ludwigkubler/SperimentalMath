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
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            if pivot == 0:
                continue
            for j in range(n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        rank = sum(1 for row in A if any(row))
        return rank
    
    def tseitin_formula(n):
        variables = [f'x{i}' for i in range(n)]
        clauses = []
        for i in range(n):
            clauses.append([variables[i]])
        for i in range(n-1):
            clauses.append([variables[i], f'~{variables[i+1]}'])
            clauses.append([f'~{variables[i]}', variables[i+1]])
        return variables, clauses
    
    def resolution_proof_length(clauses):
        stack = []
        while True:
            new_clause = None
            for i in range(len(stack)):
                for j in range(i+1, len(stack)):
                    if any(-x in stack[j] for x in stack[i]):
                        new_clause = [x for x in stack[i] if x not in [-y for y in stack[j]]]
                        break
                if new_clause:
                    break
            if not new_clause:
                return 0
            stack.append(new_clause)
    
    def config_space_rank(variables, clauses):
        n = len(variables)
        A = [[0] * (2*n + 1) for _ in range(2*n)]
        for i, var in enumerate(variables):
            A[i][i] = 1
            A[n+i][n+i] = -1
            for clause in clauses:
                if var in clause:
                    A[2*i][len(clause)-1] += 1
                elif f'~{var}' in clause:
                    A[2*n+i][len(clause)-1] -= 1
        return gaussian_elimination(A)
    
    n = random.randint(5, 40)
    variables, clauses = tseitin_formula(n)
    rank = config_space_rank(variables, clauses)
    proof_length = resolution_proof_length(clauses)
    
    if rank == 0:
        return {
            "metric_name": "Ratio",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    ratio = proof_length / (2 ** rank)
    return {
        "metric_name": "Ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 3 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        support_fraction = sum(r["instances_tested"] for r in results) / len(results)
        print(f"RESULT: SUPPORTED mean={sum(r['metric_value'] for r in results)} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")
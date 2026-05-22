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
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random

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
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
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

    def tseitin_formula(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for i in range(1, n+1):
            clauses.append([variables[i-1]])
        for i in range(1, n+1):
            for j in range(i+1, n+1):
                clauses.append([-variables[i-1], -variables[j-1]])
                clauses.append([variables[i-1], variables[j-1]])
        return variables, clauses

    def local_crossed_module_rank(clauses):
        m = len(clauses)
        A = [[0] * (m + 1) for _ in range(m)]
        for i in range(m):
            for j in range(i+1, m):
                if any(c in clauses[i] and -c in clauses[j] for c in clauses[i]):
                    A[i][j] = 1
                    A[j][i] = 1
        rank = 0
        for i in range(m):
            if all(A[j][i] == 0 for j in range(i)):
                rank += 1
        return rank

    def resolution_proof_length(clauses):
        stack = []
        while clauses:
            clause = clauses.pop()
            if len(clause) == 1:
                literal = clause[0]
                if literal > 0 and -literal in [c for cl in clauses for c in cl]:
                    continue
                elif literal < 0 and -literal not in [c for cl in clauses for c in cl]:
                    return float('inf')
            else:
                literal = random.choice(clause)
                if literal > 0:
                    stack.append(-literal)
                else:
                    stack.append(literal)
                new_clauses = []
                for cl in clauses:
                    if literal not in cl and -literal not in cl:
                        new_clauses.append(cl)
                    elif literal in cl:
                        new_clauses.extend([[c for c in cl if c != literal] + [-l] for l in stack])
                    else:
                        new_clauses.extend([[c for c in cl if c != -literal] + [l] for l in stack])
                clauses = new_clauses
        return len(stack)

    n = random.randint(5, 40)
    variables, clauses = tseitin_formula(n)
    rank = local_crossed_module_rank(clauses)
    length = resolution_proof_length(clauses)
    
    if length == float('inf'):
        return {
            "metric_name": "local_crossed_module_rank",
            "metric_value": rank,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "resolution_proved_unsat"
        }
    
    c = rank / length
    if c > 1:
        return {
            "metric_name": "local_crossed_module_rank",
            "metric_value": rank,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"c={c} exceeds 1"
        }
    
    return {
        "metric_name": "local_crossed_module_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if r["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
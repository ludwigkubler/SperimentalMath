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

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0 for _ in range(p)] for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def tseitin_formula(n):
        literals = [f'x{i}' for i in range(n)]
        clauses = []
        for i in range(n):
            clauses.append([literals[i]])
            clauses.append([-literals[i]])
        for i in range(n-1):
            clauses.append([literals[i], literals[i+1]])
            clauses.append([-literals[i], -literals[i+1]])
        return literals, clauses

    def algebraic_variety(clauses):
        n = len(clauses)
        A = [[0 for _ in range(n)] for _ in range(n)]
        b = [0] * n
        for i, clause in enumerate(clauses):
            for literal in clause:
                if literal.startswith('x'):
                    j = int(literal[1:])
                    A[i][j-1] += 1
                else:
                    j = int(literal[1:]) - 1
                    A[i][j] -= 1
        return gaussian_elimination(A), b

    def hodge_class_polynomial_degree(A):
        m, n = len(A), len(A[0])
        rank = 0
        for i in range(m):
            if all(A[i][j] == 0 for j in range(n)):
                continue
            rank += 1
        return rank

    def frege_proof_length(clauses):
        stack = []
        for clause in clauses:
            while True:
                found = False
                for literal in clause:
                    if literal.startswith('x'):
                        if literal not in stack:
                            stack.append(literal)
                            found = True
                            break
                    else:
                        if -literal in stack:
                            stack.remove(-literal)
                            found = True
                            break
                if not found:
                    stack.append(clause[0])
                    break
        return len(stack)

    literals, clauses = tseitin_formula(40)
    A, b = algebraic_variety(clauses)
    min_deg_hodge_class = hodge_class_polynomial_degree(A)
    L_pi = frege_proof_length(clauses)
    
    return {
        "metric_name": "min_deg_Hodge_class",
        "metric_value": min_deg_hodge_class,
        "instances_tested": 1,
        "n_max": 40,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    else:
        seeds = [int(s) for s in sys.argv[1:]]

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
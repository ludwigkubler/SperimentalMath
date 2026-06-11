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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + random.randint(0, m - i - 1)
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            if pivot == 0:
                continue
            for j in range(n):
                A[i][j] /= pivot
            for k in range(m):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A
    
    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def determinant(A):
        m, n = len(A), len(A[0])
        if m != n:
            return 0
        if n == 1:
            return A[0][0]
        det = Fraction(0)
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += (-1) ** j * A[0][j] * determinant(submatrix)
        return det
    
    def tseitin_formula(f, n):
        literals = list(range(-n, 0)) + list(range(1, n + 1))
        clauses = []
        for i in range(n):
            clause = [literals[i], literals[n + i]]
            clauses.append(clause)
            clause = [-literals[i], -literals[n + i]]
            clauses.append(clause)
        for i in range(n):
            for j in range(i + 1, n):
                clause = [-literals[i], -literals[j], literals[n + i + j]]
                clauses.append(clause)
                clause = [literals[i], literals[j], literals[n + i + j]]
                clauses.append(clause)
        return clauses
    
    def resolution_proof_depth(clauses):
        stack = []
        while True:
            new_clause = None
            for i in range(len(stack)):
                for j in range(i + 1, len(stack)):
                    if -stack[i][0] in stack[j]:
                        new_clause = [x for x in stack[i] if x != -stack[j][0]] + [x for x in stack[j] if x != -stack[i][0]]
                        break
                if new_clause:
                    break
            if not new_clause:
                return len(stack)
            stack.append(new_clause)
    
    def geometric_entropy(A):
        m, n = len(A), len(A[0])
        det = determinant(gaussian_elimination(A))
        entropy = 0
        for i in range(m):
            for j in range(n):
                if A[i][j] != 0:
                    entropy += -A[i][j] * math.log2(abs(A[i][j]))
        return entropy
    
    def random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    n_values = [10, 15, 20, 25, 30, 35, 40]
    results = []
    total_instances = 0
    max_n = 0
    
    for n in n_values:
        for _ in range(4):
            f = random_boolean_function(n)
            A = [[f[i * n + j] if i == j else 0 for j in range(n)] for i in range(n)]
            H_min = geometric_entropy(A)
            clauses = tseitin_formula(f, n)
            d_res = resolution_proof_depth(clauses)
            results.append({"H_min": H_min, "d_res": d_res})
            total_instances += 1
            max_n = max(max_n, n)
    
    if not results:
        return {
            "metric_name": "geometric_entropy",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max_n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    H_min_values = [r["H_min"] for r in results]
    d_res_values = [r["d_res"] for r in results]
    
    mean_H_min = sum(H_min_values) / len(H_min_values)
    mean_d_res = sum(d_res_values) / len(d_res_values)
    
    correlation = 0
    n = len(results)
    for i in range(n):
        correlation += (H_min_values[i] - mean_H_min) * (d_res_values[i] - mean_d_res)
    correlation /= (n * sum((x - mean_H_min)**2 for x in H_min_values))**0.5 * (n * sum((y - mean_d_res)**2 for y in d_res_values))**0.5
    
    return {
        "metric_name": "geometric_entropy",
        "metric_value": correlation,
        "instances_tested": total_instances,
        "n_max": max_n,
        "conjecture_holds": abs(correlation) >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if abs(r["metric_value"]) >= 0.8) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")
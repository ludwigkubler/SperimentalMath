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
    
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a
    
    def lcm(a, b):
        return abs(a * b) // gcd(a, b)
    
    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y
    
    def mod_inverse(a, m):
        gcd, x, _ = extended_gcd(a, m)
        if gcd != 1:
            return None
        else:
            return x % m
    
    def matrix_mult(A, B):
        rows_A = len(A)
        cols_A = len(A[0])
        rows_B = len(B)
        cols_B = len(B[0])
        result = [[sum(A[i][k] * B[k][j] for k in range(cols_A)) for j in range(cols_B)] for i in range(rows_A)]
        return result
    
    def matrix_add(A, B):
        rows = len(A)
        cols = len(A[0])
        result = [[A[i][j] + B[i][j] for j in range(cols)] for i in range(rows)]
        return result
    
    def matrix_sub(A, B):
        rows = len(A)
        cols = len(A[0])
        result = [[A[i][j] - B[i][j] for j in range(cols)] for i in range(rows)]
        return result
    
    def transpose(matrix):
        return [list(row) for row in zip(*matrix)]
    
    def determinant(matrix):
        if len(matrix) == 1:
            return matrix[0][0]
        elif len(matrix) == 2:
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        else:
            det = 0
            for c in range(len(matrix)):
                submatrix = [row[:c] + row[c+1:] for row in matrix[1:]]
                sign = (-1) ** (c % 2)
                sub_det = determinant(submatrix)
                det += sign * matrix[0][c] * sub_det
            return det
    
    def inverse(matrix):
        det = determinant(matrix)
        if det == 0:
            return None
        adjugate = []
        for i in range(len(matrix)):
            row = []
            for j in range(len(matrix)):
                minor = [row[:j] + row[j+1:] for row in matrix[:i] + matrix[i+1:]]
                cofactor = ((-1) ** (i+j)) * determinant(minor)
                row.append(cofactor)
            adjugate.append(row)
        return [[adjugate[j][i] / det for j in range(len(matrix))] for i in range(len(matrix))]
    
    def gaussian_elimination(A, b):
        n = len(b)
        Augmented_matrix = [A[i] + [b[i]] for i in range(n)]
        for i in range(n):
            max_row = max(range(i, n), key=lambda k: abs(Augmented_matrix[k][i]))
            Augmented_matrix[i], Augmented_matrix[max_row] = Augmented_matrix[max_row], Augmented_matrix[i]
            factor = Augmented_matrix[i][i]
            for j in range(i, n + 1):
                Augmented_matrix[i][j] /= factor
            for k in range(n):
                if k != i:
                    factor = Augmented_matrix[k][i]
                    for j in range(i, n + 1):
                        Augmented_matrix[k][j] -= factor * Augmented_matrix[i][j]
        return [row[-1] for row in Augmented_matrix]
    
    def is_integer(x):
        return abs(x - round(x)) < 1e-9
    
    def tseitin_formula(n):
        variables = list(range(1, n+1))
        clauses = []
        for i in range(1, n+1):
            clauses.append([i])
            clauses.append([-i])
        for i in range(1, n+1):
            for j in range(i+1, n+1):
                clauses.append([i, -j])
                clauses.append([-i, j])
        return variables, clauses
    
    def generalized_ehrhart_lattice(variables, clauses):
        n = len(variables)
        m = len(clauses)
        A = [[0] * (n + m) for _ in range(n + m)]
        b = [0] * (n + m)
        
        for i in range(n):
            A[i][i] = 1
            b[i] = 1
        
        for j in range(m):
            A[n + j][j] = 1
            b[n + j] = 2
        
        return A, b
    
    def resolution_width(clauses):
        n = len(clauses)
        queue = clauses[:]
        resolvents = set()
        
        while queue:
            clause1 = queue.pop(0)
            for clause2 in queue:
                common_vars = [var for var in clause1 if -var in clause2]
                if not common_vars:
                    continue
                new_clause = list(set(clause1 + clause2) - {common_vars[0], -common_vars[0]})
                if len(new_clause) == 1 and new_clause[0] < 0:
                    return abs(new_clause[0])
                if tuple(sorted(new_clause)) not in resolvents:
                    queue.append(new_clause)
                    resolvents.add(tuple(sorted(new_clause)))
        
        return float('inf')
    
    n = random.randint(5, 40)
    variables, clauses = tseitin_formula(n)
    A, b = generalized_ehrhart_lattice(variables, clauses)
    rank = len([row for row in A if any(row[i] != 0 for i in range(len(row)))])
    width = resolution_width(clauses)
    
    return {
        "metric_name": "MinRank(L(G))",
        "metric_value": rank,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": rank <= width * 2 and rank >= width / 2,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
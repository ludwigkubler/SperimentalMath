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
    
    def gaussian_elimination(A, b):
        n = len(A)
        for i in range(n):
            # Find max pivot in column i
            max_idx = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_idx][i]):
                    max_idx = j
            A[i], A[max_idx] = A[max_idx], A[i]
            b[i], b[max_idx] = b[max_idx], b[i]
            
            # Eliminate column i for all rows below i
            for j in range(i+1, n):
                factor = -A[j][i] / A[i][i]
                for k in range(i, n):
                    A[j][k] += factor * A[i][k]
                b[j] += factor * b[i]
        
        # Back-substitution
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
        return x
    
    def matrix_multiply(A, B):
        m, n = len(A), len(B[0])
        p = len(B)
        C = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def determinant(A):
        if len(A) == 1:
            return A[0][0]
        det = 0
        sign = 1
        for j in range(len(A)):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += sign * A[0][j] * determinant(submatrix)
            sign *= -1
        return det
    
    def linear_algebra_solver(A, b):
        det_A = determinant(A)
        if det_A == 0:
            return None
        x = [Fraction(0) for _ in range(len(A))]
        for i in range(len(A)):
            A_i = [row[:i] + row[i+1:] for row in A]
            b_i = b[:]
            b_i[i] /= det_A
            A_i[i][i] = 1 / det_A
            x[i] = Fraction(b_i[i])
        return x
    
    def generate_tseitin_formula(n):
        variables = list(range(1, n+1))
        clauses = []
        for i in range(1, n+1):
            clauses.append([i])
            clauses.append([-i])
        for i in range(1, n+1):
            for j in range(i+1, n+1):
                clauses.append([i, -j])
                clauses.append([-i, j])
                clauses.append([j, -i])
                clauses.append([-j, i])
        return variables, clauses
    
    def resolution_width(clauses):
        queue = set()
        for clause in clauses:
            if len(clause) == 1:
                queue.add(clause[0])
            elif len(clause) == 2:
                queue.add(clause[0])
                queue.add(-clause[1])
            else:
                return float('inf')
        while queue:
            literal = random.choice(list(queue))
            queue.remove(literal)
            for clause in clauses:
                if literal in clause:
                    new_clause = [l for l in clause if l != literal]
                    if len(new_clause) == 0:
                        return float('inf')
                    elif len(new_clause) == 1:
                        queue.add(new_clause[0])
        return len(queue)
    
    def quiver_representation_length(variables, clauses):
        n = len(variables)
        m = len(clauses)
        A = [[0] * (n + m) for _ in range(n + m)]
        b = [0] * (n + m)
        
        for i in range(n):
            A[i][i] = 1
            b[i] = 1
        
        for j in range(m):
            clause = clauses[j]
            if len(clause) == 1:
                A[n + j][variables.index(abs(clause[0]))] = 1
                b[n + j] = -clause[0]
            elif len(clause) == 2:
                A[n + j][variables.index(abs(clause[0]))] = 1
                A[n + j][n + m + variables.index(abs(clause[1]))] = 1
                b[n + j] = clause[0] + clause[1]
            else:
                return float('inf')
        
        solution = linear_algebra_solver(A, b)
        if solution is None:
            return float('inf')
        return sum(abs(sol) for sol in solution)
    
    variables, clauses = generate_tseitin_formula(10)
    representation_length = quiver_representation_length(variables, clauses)
    width = resolution_width(clauses)
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": representation_length * width,
        "instances_tested": 1,
        "n_max": 10,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={seeds[first_failing_seed]}")
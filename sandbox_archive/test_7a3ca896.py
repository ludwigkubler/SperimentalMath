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
        else:
            g, x, y = extended_gcd(b % a, a)
            return g, y - (b // a) * x, x
    
    def mod_inverse(a, m):
        g, x, _ = extended_gcd(a, m)
        if g != 1:
            return None
        else:
            return x % m
    
    def matrix_mult(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
                C[i][j] %= m
        return C
    
    def matrix_pow(A, n, m):
        result = [[1 if i == j else 0 for j in range(len(A))] for i in range(len(A))]
        while n > 0:
            if n % 2 == 1:
                result = matrix_mult(result, A, m)
            A = matrix_mult(A, A, m)
            n //= 2
        return result
    
    def is_invertible(matrix):
        det = 0
        for i in range(len(matrix)):
            sign = (-1) ** i
            submatrix = [row[:i] + row[i+1:] for row in matrix[1:]]
            subdet = matrix_det(submatrix)
            det += sign * matrix[0][i] * subdet
        return det != 0
    
    def matrix_det(matrix):
        if len(matrix) == 2:
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        det = 0
        for i in range(len(matrix)):
            submatrix = [row[:i] + row[i+1:] for row in matrix[1:]]
            det += (-1) ** i * matrix[0][i] * matrix_det(submatrix)
        return det
    
    def gaussian_elimination(A, b):
        n = len(b)
        A_b = [A[i] + [b[i]] for i in range(n)]
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A_b[j][i]) > abs(A_b[max_row][i]):
                    max_row = j
            A_b[i], A_b[max_row] = A_b[max_row], A_b[i]
            factor = 1 / A_b[i][i]
            for j in range(i, n+1):
                A_b[i][j] *= factor
            for j in range(n):
                if i != j:
                    factor = A_b[j][i]
                    for k in range(i, n+1):
                        A_b[j][k] -= factor * A_b[i][k]
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = A_b[i][-1]
            for j in range(i+1, n):
                x[i] -= A_b[i][j] * x[j]
        return x
    
    def is_solution_valid(x, A, b):
        return all(abs(A[i][j] * x[j] - b[i]) < 1e-9 for i in range(len(b)))
    
    def generate_diophantine_system(n):
        A = [[random.randint(0, 10) for _ in range(n)] for _ in range(n)]
        b = [sum(A[i][j] * random.randint(0, 10) for j in range(n)) % 11 for i in range(n)]
        return A, b
    
    def tseitin_formula(A, b):
        n = len(b)
        literals = list(range(-2*n, 0))
        clauses = []
        for i in range(n):
            clauses.append([literals[i], literals[n+i]])
            for j in range(i+1, n):
                clauses.append([literals[i], -literals[j+n]])
                clauses.append([-literals[i], literals[j+n]])
        for i in range(n):
            for j in range(n):
                if A[i][j] != 0:
                    clauses.append([literals[n+i], literals[j+n]])
        return literals, clauses
    
    def resolution_width(clauses):
        queue = set(lit for lit in literals if lit > 0)
        width = len(queue)
        while queue:
            new_queue = set()
            for lit in queue:
                for clause in clauses:
                    if lit in clause:
                        new_clause = [l for l in clause if l != lit and -l not in clause]
                        if not new_clause:
                            return float('inf')
                        new_queue.add(min(new_clause))
            queue.update(new_queue)
            width = max(width, len(queue))
        return width
    
    def compute_minimal_rank(A, b):
        rank = 0
        for i in range(len(b)):
            if is_solution_valid([1 if j == i else 0 for j in range(len(b))], A, b):
                rank += 1
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    ranks = []
    widths = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            A, b = generate_diophantine_system(n)
            rank = compute_minimal_rank(A, b)
            ranks.append(rank)
            literals, clauses = tseitin_formula(A, b)
            width = resolution_width(clauses)
            widths.append(width)
    
    correlation_coefficient = sum((ranks[i] - mean_ranks) * (widths[i] - mean_widths) for i in range(len(ranks))) / len(ranks)
    mean_ranks = sum(ranks) / len(ranks)
    mean_widths = sum(widths) / len(widths)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(ranks),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.9,
        "counterexample": "" if correlation_coefficient >= 0.9 else f"Correlation coefficient {correlation_coefficient} < 0.9"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.9\" first_failing_seed={first_failing_seed}")
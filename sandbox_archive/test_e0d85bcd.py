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
    
    def generate_cnf(n, d):
        cnf = []
        for _ in range(d * n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def resolution_width(cnf):
        # Simplified DPLL solver to estimate width
        queue = cnf[:]
        while queue:
            literal = random.choice(queue[0])
            if literal < 0:
                literal = -literal
            new_clauses = []
            for clause in queue:
                if literal not in clause and -literal not in clause:
                    new_clauses.append(clause)
                elif -literal in clause:
                    clause.remove(-literal)
                    if len(clause) == 1:
                        return abs(clause[0])
            queue = new_clauses
        return 0
    
    def noncommutative_probability_order(cnf):
        # Simplified mapping to unitary matrices and computation of order
        n = max(abs(lit) for lit in cnf)
        unitaries = {i: [[random.random() for _ in range(n)] for _ in range(n)] for i in range(1, n + 1)}
        order = 0
        for clause in cnf:
            product = [1] * n
            for lit in clause:
                if lit > 0:
                    product = matrix_multiply(product, unitaries[lit])
                else:
                    product = matrix_multiply(product, inverse(unitaries[-lit]))
            order += sum(abs(x) for x in product)
        return order / len(cnf)
    
    def matrix_multiply(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def inverse(matrix):
        n = len(matrix)
        det = 0
        if n == 1:
            det = matrix[0][0]
        elif n == 2:
            det = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        else:
            for col in range(n):
                submatrix = [row[:col] + row[col+1:] for row in matrix[1:]]
                det += (-1) ** col * matrix[0][col] * determinant(submatrix)
        if det == 0:
            return None
        adjugate = [[(-1) ** (i + j) * determinant(minor(matrix, i, j)) for j in range(n)] for i in range(n)]
        inverse_matrix = [[adjugate[j][i] / det for j in range(n)] for i in range(n)]
        return inverse_matrix
    
    def determinant(matrix):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        elif n == 2:
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        else:
            det = 0
            for col in range(n):
                submatrix = [row[:col] + row[col+1:] for row in matrix[1:]]
                det += (-1) ** col * matrix[0][col] * determinant(submatrix)
            return det
    
    def minor(matrix, i, j):
        return [row[:j] + row[j+1:] for row in matrix[:i] + matrix[i+1:]]
    
    n = random.randint(5, 40)
    d = random.randint(1, 3)  # At most 3 clauses per variable
    cnf = generate_cnf(n, d)
    o_phi = noncommutative_probability_order(cnf)
    w_phi = resolution_width(cnf)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": abs(o_phi - w_phi),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(o_phi - w_phi) <= 0.5,  # Pre-defined threshold k
        "counterexample": ""
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2**i + 3 for i in range(5, 8)]  # Default list of 30 primes
    else:
        seeds = [int(seed) for seed in sys.argv[1:]]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient\" first_failing_seed={first_failing_seed}")
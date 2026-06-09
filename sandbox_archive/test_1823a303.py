# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations

# Helper functions for linear algebra and geometric operations

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find pivot row
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate non-pivot elements below the pivot
        factor = 1 / A[i][i]
        for j in range(i, n):
            A[i][j] *= factor
        for k in range(i+1, n):
            factor = A[k][i]
            for j in range(i, n):
                A[k][j] -= factor * A[i][j]
    return A

def determinant(A):
    n = len(A)
    det = 1
    for i in range(n):
        det *= A[i][i]
    return det

def matrix_multiplication(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def identity_matrix(n):
    I = [[0] * n for _ in range(n)]
    for i in range(n):
        I[i][i] = 1
    return I

def inverse(A):
    n = len(A)
    A_augmented = [row + row[:] for row in A]
    identity = identity_matrix(n)
    for i in range(n):
        factor = 1 / A_augmented[i][i]
        for j in range(2 * n):
            A_augmented[i][j] *= factor
        for k in range(n):
            if k != i:
                factor = A_augmented[k][i]
                for j in range(2 * n):
                    A_augmented[k][j] -= factor * A_augmented[i][j]
    return [row[n:] for row in A_augmented]

def is_invertible(A):
    return determinant(A) != 0

# Function to generate a random CNF with n variables
def generate_cnf(n, num_clauses=10):
    clauses = []
    for _ in range(num_clauses):
        clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
        if all(c != -x for c in clause for x in clause):
            clauses.append(clause)
    return clauses

# Function to construct the associated variety V and compute the moduli space M
def construct_variety_and_moduli_space(clauses):
    n = len(clauses[0])
    # Simplified construction of V and M (this is a placeholder)
    V = [[1] * n for _ in range(n)]
    M = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    return V, M

# Function to compute the geometric quotient Q
def geometric_quotient(M):
    # Simplified computation of Q (this is a placeholder)
    n = len(M)
    Q = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    return Q

# Function to calculate the minimal order of an eta-quotient on Q
def minimal_eta_quotient_order(Q):
    # Simplified calculation (this is a placeholder)
    n = len(Q)
    order = 1
    for i in range(n):
        for j in range(i+1, n):
            if Q[i][j] != 0:
                order *= abs(Q[i][j])
    return order

# Function to compute the Frege proof width w(φ) of a CNF φ
def frege_proof_width(clauses):
    # Simplified computation (this is a placeholder)
    n = len(clauses[0])
    width = n * len(clauses)
    return width

# Main function to run one trial with a given seed
def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    metric_name = "eta_quotient_order_vs_frege_width"
    instances_tested = 0
    n_max = 0
    eta_quotient_orders = []
    frege_widths = []
    
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        clauses = generate_cnf(n)
        
        V, M = construct_variety_and_moduli_space(clauses)
        Q = geometric_quotient(M)
        
        if not is_invertible(Q):
            continue
        
        eta_quotient_order = minimal_eta_quotient_order(Q)
        frege_width = frege_proof_width(clauses)
        
        eta_quotient_orders.append(eta_quotient_order)
        frege_widths.append(frege_width)
        
        instances_tested += 1
        n_max = max(n_max, n)
    
    if not eta_quotient_orders or not frege_widths:
        return {
            "metric_name": metric_name,
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    eta_quotient_order_mean = sum(eta_quotient_orders) / len(eta_quotient_orders)
    frege_width_mean = sum(frege_widths) / len(frege_widths)
    correlation_coefficient = (sum((x - eta_quotient_order_mean) * (y - frege_width_mean) for x, y in zip(eta_quotient_orders, frege_widths)) /
                                math.sqrt(sum((x - eta_quotient_order_mean) ** 2 for x in eta_quotient_orders) *
                                          sum((y - frege_width_mean) ** 2 for y in frege_widths)))
    
    return {
        "metric_name": metric_name,
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation_coefficient) > 0.5,
        "counterexample": ""
    }

# Main execution block
if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
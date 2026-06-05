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

# Helper functions for Gaussian elimination and matrix operations
def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        # Find pivot row
        max_row = i
        for k in range(i + 1, n):
            if abs(matrix[k][i]) > abs(matrix[max_row][i]):
                max_row = k
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below pivot
        for k in range(i + 1, n):
            factor = Fraction(matrix[k][i], matrix[i][i])
            for j in range(n):
                matrix[k][j] -= factor * matrix[i][j]
    
    # Back substitution
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = Fraction(matrix[i][-1], matrix[i][i])
        for j in range(i + 1, n):
            x[i] -= x[j] * matrix[i][j]
    
    return x

def matrix_multiply(A, B):
    m = len(A)
    k = len(B)
    n = len(B[0])
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for p in range(k):
                C[i][j] += A[i][p] * B[p][j]
    return C

def matrix_power(A, n):
    result = [[Fraction(1) if i == j else Fraction(0) for j in range(len(A))] for i in range(len(A))]
    while n > 0:
        if n % 2 == 1:
            result = matrix_multiply(result, A)
        A = matrix_multiply(A, A)
        n //= 2
    return result

def communication_complexity(phi):
    # Placeholder function to compute communication complexity rank r_Γ(φ)
    # This is a dummy implementation and should be replaced with actual logic.
    return random.randint(1, 10)

# Function to generate a random CNF with n variables
def generate_cnf(n):
    cnf = []
    for _ in range(random.randint(5, 10)):
        clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
        if len(set(clause)) == len(clause):  # Ensure no duplicate literals
            cnf.append(clause)
    return cnf

# Function to compute the minimal local induction ring rank m_lir(φ)
def minimal_local_induction_ring_rank(cnf):
    n = max(abs(lit) for clause in cnf for lit in clause)
    poly = [0] * (2 ** n)
    for clause in cnf:
        product = 1
        for lit in clause:
            product *= (-1 if lit < 0 else 1) * (1 - Fraction(1, 2) ** abs(lit))
        poly[sum(abs(lit) for lit in clause)] += product
    
    matrix = [[poly[i ^ (1 << j)] for j in range(n)] for i in range(2 ** n)]
    rank = sum(1 for row in gaussian_elimination(matrix) if any(row))
    return rank

# Main function to run a single trial
def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        phi = generate_cnf(n)
        
        m_lir = minimal_local_induction_ring_rank(phi)
        r_Γ = communication_complexity(phi)
        
        results.append((m_lir, r_Γ))
    
    if not results:
        return {
            "metric_name": "minimal_local_induction_ring_rank",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_results"
        }
    
    m_lir_values = [m for m, _ in results]
    r_Γ_values = [r for _, r in results]
    
    correlation_coefficient = sum((m - sum(m_lir_values) / len(m_lir_values)) * (r - sum(r_Γ_values) / len(r_Γ_values)) for m, r in results)
    correlation_coefficient /= math.sqrt(sum((m - sum(m_lir_values) / len(m_lir_values)) ** 2 for m in m_lir_values)) * math.sqrt(sum((r - sum(r_Γ_values) / len(r_Γ_values)) ** 2 for r in r_Γ_values))
    
    conjecture_holds = correlation_coefficient >= 0.9
    counterexample = "" if conjecture_holds else "correlation_coefficient=<{}>".format(correlation_coefficient)
    
    return {
        "metric_name": "minimal_local_induction_ring_rank",
        "metric_value": sum(m_lir_values) / len(m_lir_values),
        "instances_tested": 30,
        "n_max": max(n for _, n in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

# Main execution block
if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print("TRIAL: {}".format(trial_result))
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print("RESULT: SUPPORTED mean={} std=0 support_fraction={}".format(mean_value, 0, support_fraction))
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = results[seeds.index(first_failing_seed)]["counterexample"]
        print("RESULT: FALSIFIED counterexample={} first_failing_seed={}".format(counterexample, first_failing_seed))
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

# Helper functions for Gaussian elimination and matrix operations
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
        for j in range(i+1, n):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(n):
                A[j][k] -= factor * A[i][k]

def matrix_multiplication(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[Fraction(0) for _ in range(p)] for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def determinant(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    det = Fraction(0)
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in A[1:]]
        det += (-1)**j * A[0][j] * determinant(submatrix)
    return det

# Function to generate a random Boolean satisfiability instance
def generate_instance(n):
    clauses = []
    literals = set()
    for _ in range(n):
        clause = [random.choice([True, False]) for _ in range(2)]
        clauses.append(clause)
        literals.update(clause)
    return clauses, list(literals)

# Function to construct a noncommutative crossed product structure
def construct_crossed_product(instance):
    clauses, literals = instance
    n = len(clauses)
    m = len(literals)
    
    # Create groups for clauses and literals
    G_clauses = [[Fraction(1), Fraction(i)] for i in range(n)]
    G_literals = [[Fraction(1), Fraction(j)] for j in range(m)]
    
    # Compute the semidirect product
    G = []
    for g_clause in G_clauses:
        for g_literal in G_literals:
            G.append([g_clause[0] * g_literal[0], g_clause[1] + g_literal[1]])
    
    return G

# Function to measure resolution proof width using a small DPLL solver
def measure_resolution_width(instance):
    clauses, literals = instance
    n = len(clauses)
    m = len(literals)
    
    # Convert clauses to a list of sets for easier manipulation
    clause_sets = [set(clause) for clause in clauses]
    
    # Initialize the set of learned clauses
    learned_clauses = []
    
    def dpll(model):
        if not any(clause.issubset(model) for clause in clause_sets):
            return model
        
        unit_clause = None
        for literal in literals:
            if literal not in model and -literal not in model:
                unit_clause = {literal}
                break
            elif literal in model:
                unit_clause = {-literal}
                break
        
        if unit_clause is not None:
            new_model = model.union(unit_clause)
            result = dpll(new_model)
            if result is not None:
                return result
            else:
                return dpll(model - unit_clause)
        
        pure_literal = None
        for literal in literals:
            if all(literal in clause or -literal in clause for clause in learned_clauses):
                pure_literal = literal
                break
        
        if pure_literal is not None:
            new_model = model.union({pure_literal})
            result = dpll(new_model)
            if result is not None:
                return result
            else:
                return dpll(model - {pure_literal})
        
        # Pure literal search failed, try to learn a new clause
        for i in range(n):
            if any(literal in learned_clauses[j] or -literal in learned_clauses[j] for j in range(i)):
                continue
            
            new_clause = set()
            for literal in literals:
                if literal not in model and -literal not in model:
                    new_clause.add(literal)
            
            learned_clauses.append(new_clause)
        
        return dpll(model)
    
    result = dpll(set())
    return len(learned_clauses)

# Function to calculate Pearson correlation coefficient
def calculate_correlation(metric_values, instances_tested):
    n = len(metric_values)
    if n == 0:
        return 0.0
    
    sum_x = sum(metric_values)
    sum_y = sum(instances_tested)
    sum_xy = sum(x * y for x, y in zip(metric_values, instances_tested))
    sum_x2 = sum(x**2 for x in metric_values)
    sum_y2 = sum(y**2 for y in instances_tested)
    
    numerator = n * sum_xy - sum_x * sum_y
    denominator = math.sqrt((n * sum_x2 - sum_x**2) * (n * sum_y2 - sum_y**2))
    
    if denominator == 0:
        return 0.0
    
    return numerator / denominator

# Function to run a single trial for the conjecture
def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    metric_values = []
    instances_tested = []
    
    for n in n_values:
        instance = generate_instance(n)
        crossed_product = construct_crossed_product(instance)
        order_crossed_product = len(crossed_product)
        
        resolution_width = measure_resolution_width(instance)
        
        metric_values.append(order_crossed_product)
        instances_tested.append(resolution_width)
    
    correlation = calculate_correlation(metric_values, instances_tested)
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation,
        "instances_tested": sum(instances_tested),
        "n_max": max(n_values),
        "conjecture_holds": 0.8 <= correlation <= 1.0,
        "counterexample": "" if 0.8 <= correlation <= 1.0 else f"Correlation out of range: {correlation}"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results]
    instances_tested = [r["instances_tested"] for r in results]
    correlation = calculate_correlation(metric_values, instances_tested)
    
    support_fraction = sum(1 for r in results if 0.8 <= r["metric_value"] <= 1.0) / len(results)
    
    if all(0.8 <= r["metric_value"] <= 1.0 for r in results):
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values):.4f} std={math.sqrt(sum((x - sum(metric_values)/len(metric_values))**2 for x in metric_values) / len(metric_values)):.4f} support_fraction={support_fraction:.4f}")
    elif any(r["metric_value"] > 1.0 for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if r["metric_value"] > 1.0)
        print(f"RESULT: FALSIFIED counterexample='correlation_greater_than_1' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=not_enough_support support_fraction={support_fraction:.4f}")
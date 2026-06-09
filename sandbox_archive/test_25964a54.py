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

def generate_sat_instance(n):
    clauses = []
    for _ in range(2 * n):
        clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
        if all(clause[i] == -clause[j] for i in range(n) for j in range(i + 1, n)):
            continue
        clauses.append(clause)
    return clauses

def generate_noncommutative_space(clauses):
    # Simplified encoding of logical gates as operators
    operators = {i: [] for i in range(2 * len(clauses))}
    for clause in clauses:
        for literal in clause:
            if literal > 0:
                operators[literal].append(literal)
            else:
                operators[-literal].append(-literal)
    return operators

def compute_geometric_entropy(noncommutative_space):
    # Simplified computation of geometric entropy using spectral gap
    adjacency_matrix = [[0] * len(noncommutative_space) for _ in range(len(noncommutative_space))]
    for i, ops_i in noncommutative_space.items():
        for j, ops_j in noncommutative_space.items():
            if i == j:
                adjacency_matrix[i][j] = len(ops_i)
            else:
                common_ops = set(ops_i).intersection(set(ops_j))
                adjacency_matrix[i][j] = len(common_ops)
    
    # Gaussian elimination to find eigenvalues
    n = len(adjacency_matrix)
    identity_matrix = [[Fraction(i == j, 1) for i in range(n)] for j in range(n)]
    augmented_matrix = [row + col for row, col in zip(adjacency_matrix, identity_matrix)]
    for i in range(n):
        pivot = augmented_matrix[i][i]
        if pivot == Fraction(0, 1):
            return None
        for j in range(i, n * 2):
            augmented_matrix[i][j] /= pivot
    
    for i in range(n - 1, 0, -1):
        for j in range(i):
            factor = augmented_matrix[j][i]
            for k in range(n * 2):
                augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
    
    eigenvalues = [augmented_matrix[i][i + n] for i in range(n)]
    return max(eigenvalues) - min(eigenvalues)

def compute_resolution_proof_width(clauses):
    # Simplified computation of resolution proof width
    width = 0
    for clause in clauses:
        width = max(width, len(set(abs(lit) for lit in clause)))
    return width

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_entropy = 0
    total_width = 0
    
    for n in n_values:
        for _ in range(5):  # Test each size with 5 different instances
            clauses = generate_sat_instance(n)
            noncommutative_space = generate_noncommutative_space(clauses)
            entropy = compute_geometric_entropy(noncommutative_space)
            if entropy is None:
                continue
            width = compute_resolution_proof_width(clauses)
            
            total_entropy += entropy
            total_width += width
            instances_tested += 1
    
    mean_entropy = total_entropy / instances_tested
    mean_width = total_width / instances_tested
    
    correlation_coefficient = (instances_tested * sum(entropy * width for entropy, width in zip([mean_entropy] * instances_tested, [mean_width] * instances_tested)) - 
                               instances_tested * mean_entropy * mean_width) / ((instances_tested - 1) * math.sqrt(instances_tested * sum((entropy - mean_entropy) ** 2 for entropy in [mean_entropy] * instances_tested) * sum((width - mean_width) ** 2 for width in [mean_width] * instances_tested)))
    
    conjecture_holds = correlation_coefficient >= 0.8
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
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
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
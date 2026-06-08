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
    
    def generate_monomial_representation(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_projective_variety(monomial):
        n = len(monomial)
        variety = []
        for i in range(2**n):
            point = [int(x) for x in format(i, f'0{n}b')]
            if all(point[j] == monomial[j] or point[j] == 1 - monomial[j] for j in range(n)):
                variety.append(point)
        return variety
    
    def compute_hodge_index(variety):
        n = len(variety[0])
        matrix = [[0] * n for _ in range(n)]
        for point in variety:
            for i in range(n):
                for j in range(i, n):
                    if point[i] != point[j]:
                        matrix[i][j] += 1
                        matrix[j][i] += 1
        det = determinant(matrix)
        return abs(det) ** (1/n)
    
    def determinant(matrix):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            det += (-1) ** j * matrix[0][j] * determinant(submatrix)
        return det
    
    def tseitin_formula(monomial):
        n = len(monomial)
        literals = list(range(1, 2*n + 1))
        clauses = []
        for i in range(n):
            clauses.append([literals[i], -literals[n+i]])
        for i in range(n):
            for j in range(i+1, n):
                clauses.append([-literals[i], -literals[j], literals[2*n]])
                clauses.append([-literals[i], literals[j], literals[2*n]])
                clauses.append([literals[i], -literals[j], literals[2*n]])
                clauses.append([literals[i], literals[j], literals[2*n]])
        return clauses
    
    def resolution_proof_width(clauses):
        n = len(clauses)
        queue = [set(clause) for clause in clauses]
        while True:
            new_clauses = []
            for i in range(n):
                for j in range(i+1, n):
                    if not (queue[i] & queue[j]):
                        continue
                    diff = queue[i].symmetric_difference(queue[j])
                    if len(diff) == 2:
                        new_clause = list(diff)
                        if new_clause not in queue and new_clause not in new_clauses:
                            new_clauses.append(new_clause)
            if not new_clauses:
                break
            queue.extend(new_clauses)
        return len(queue)
    
    n_values = [5, 10, 15, 20, 30, 40]
    h_values = []
    w_values = []
    
    for n in n_values:
        monomial = generate_monomial_representation(n)
        variety = compute_projective_variety(monomial)
        h_value = compute_hodge_index(variety)
        h_values.append(h_value)
        
        clauses = tseitin_formula(monomial)
        w_value = resolution_proof_width(clauses)
        w_values.append(w_value)
    
    if len(h_values) < 30 or len(w_values) < 30:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": len(h_values),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_h = sum(h_values) / len(h_values)
    mean_w = sum(w_values) / len(w_values)
    covariance = sum((h - mean_h) * (w - mean_w) for h, w in zip(h_values, w_values)) / len(h_values)
    variance_h = sum((h - mean_h) ** 2 for h in h_values) / len(h_values)
    variance_w = sum((w - mean_w) ** 2 for w in w_values) / len(w_values)
    pearson_corr_coeff = covariance / (math.sqrt(variance_h) * math.sqrt(variance_w))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_corr_coeff,
        "instances_tested": 30,
        "n_max": max(n_values),
        "conjecture_holds": pearson_corr_coeff >= 0.8,
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
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None])
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None]))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
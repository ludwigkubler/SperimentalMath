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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + max(range(i, m), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(n):
                if j != i:
                    factor = A[j][i] / A[i][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def xor_and_tree_width(circuit):
        if not circuit:
            return 0
        if len(circuit) == 1:
            return 1
        left = circuit[0]
        right = circuit[1:]
        return max(xor_and_tree_width(left), xor_and_tree_width(right)) + 1

    def tseitin_formula(G):
        n = len(G)
        variables = {f'x{i}': i for i in range(n)}
        clauses = []
        for i in range(n):
            clauses.append([variables[f'x{i}']])
        for i in range(n):
            for j in range(i + 1, n):
                if G[i][j]:
                    clauses.append([-variables[f'x{i}'], -variables[f'x{j}']])
        return clauses

    def local_cohomology_rank(G):
        n = len(G)
        A = [[0] * (n + 1) for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                if G[i][j]:
                    A[i][j] = 1
                    A[j][i] = 1
        A[-1][:n] = [1] * n
        rank = 0
        for row in gaussian_elimination(A):
            if any(row):
                rank += 1
        return rank

    def generate_geometric_langlands_lattice(n):
        G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            G[i][i] = 0
        return G

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        total_tree_width = 0
        total_delta_G = 0
        
        for _ in range(5):  # Ensure at least 5 instances per seed
            G = generate_geometric_langlands_lattice(n)
            delta_G = local_cohomology_rank(G)
            circuit = tseitin_formula(G)
            tree_width = xor_and_tree_width(circuit)
            
            instances_tested += 1
            total_tree_width += tree_width
            total_delta_G += delta_G
        
        mean_tree_width = total_tree_width / instances_tested
        mean_delta_G = total_delta_G / instances_tested
        correlation_coefficient = (instances_tested * sum(tree_width * delta_G for tree_width, delta_G in zip(results, results)) - 
                                   mean_tree_width * sum(results) - mean_delta_G * sum(results)) / \
                                  math.sqrt((instances_tested * sum(tree_width**2 for tree_width in results) - mean_tree_width**2) *
                                            (instances_tested * sum(delta_G**2 for delta_G in results) - mean_delta_G**2))
        
        results.append(correlation_coefficient)
    
    metric_value = sum(results) / len(results)
    conjecture_holds = all(abs(coeff) >= 0.8 for coeff in results) and metric_value >= 0.7
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **trial_result}}")
        results.append(trial_result["metric_value"])
    
    mean_metric_value = sum(results) / len(results)
    support_fraction = sum(1 for r in results if abs(r) >= 0.8) / len(results)
    
    if all(abs(r) >= 0.8 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(abs(r) < 0.8 for r in results):
        first_failing_seed = seeds[results.index(next(r for r in results if abs(r) < 0.8))]
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unsupported_operation")
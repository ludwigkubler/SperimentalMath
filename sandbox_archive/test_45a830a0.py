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
    
    def generate_random_circuit(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def cocomplex(circuit):
        n = len(circuit)
        cocomplex_matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if circuit[i] != circuit[j]:
                    cocomplex_matrix[i][j] = 1
                    cocomplex_matrix[j][i] = 1
        return cocomplex_matrix
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            max_row = i
            for j in range(i + 1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            if matrix[i][i] == 0:
                return None
            for j in range(i + 1, n):
                factor = Fraction(matrix[j][i], matrix[i][i])
                for k in range(n):
                    matrix[j][k] -= factor * matrix[i][k]
        rank = sum(1 for row in matrix if any(row))
        return rank
    
    def resolution_refutation_size(circuit):
        n = len(circuit)
        clauses = []
        for i in range(n):
            clauses.append([i, -i])
        refutation_size = 0
        while True:
            new_clause = None
            for clause1 in clauses:
                for clause2 in clauses:
                    if set(clause1) & set(clause2):
                        continue
                    new_clause = [x for x in clause1 if x not in clause2]
                    if len(new_clause) == 0:
                        return refutation_size
                    break
                if new_clause is not None:
                    break
            if new_clause is None:
                return refutation_size
            clauses.append(new_clause)
            refutation_size += 1
    
    n_values = [5, 10, 15, 20, 30, 40]
    metric_values = []
    
    for n in n_values:
        circuit = generate_random_circuit(n)
        cocomplex_matrix = cocomplex(circuit)
        rank = gaussian_elimination(cocomplex_matrix)
        if rank is None:
            continue
        t_star = resolution_refutation_size(circuit)
        metric_values.append((math.log2(t_star), rank))
    
    if len(metric_values) < 30:
        return {
            "metric_name": "Spearman Rank Correlation",
            "metric_value": None,
            "instances_tested": len(metric_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    def spearman_rank_correlation(data):
        n = len(data)
        ranks = {value: rank for rank, (value, _) in enumerate(sorted(set(value for value, _ in data)), start=1)}
        sorted_data = [(ranks[value], rank) for value, rank in data]
        sorted_data.sort(key=lambda x: x[0])
        sorted_ranks = [rank for _, rank in sorted_data]
        return 1 - (6 * sum((sorted_ranks[i] - i + 1)**2 for i in range(n)) / (n**3 - n))
    
    correlation = spearman_rank_correlation(metric_values)
    conjecture_holds = correlation >= 0.8
    counterexample = "" if conjecture_holds else "correlation < 0.5"
    
    return {
        "metric_name": "Spearman Rank Correlation",
        "metric_value": correlation,
        "instances_tested": len(metric_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(r["metric_value"] < 0.5 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["metric_value"] < 0.5)
        print(f"RESULT: FALSIFIED counterexample='correlation < 0.5' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")
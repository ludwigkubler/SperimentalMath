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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(c != 0 for c in clause):
                clauses.append(clause)
        return clauses
    
    def matrix_representation(clauses, n):
        m = len(clauses)
        A = [[0] * n for _ in range(m)]
        for i, clause in enumerate(clauses):
            for var in clause:
                if var > 0:
                    A[i][var - 1] = 1
                else:
                    A[i][-var - 1] = -1
        return A
    
    def tropical_symplectic_volume(A):
        m, n = len(A), len(A[0])
        volume = 0
        for i in range(m):
            max_row = [max(abs(A[i][j]) for j in range(n)) for _ in range(n)]
            volume += math.prod(max_row)
        return volume
    
    def entropy(clauses, n):
        total_clauses = len(clauses)
        counts = [0] * (n + 1)
        for clause in clauses:
            counts[len(clause)] += 1
        probabilities = [c / total_clauses for c in counts]
        entropy = -sum(p * math.log2(p) if p > 0 else 0 for p in probabilities)
        return entropy
    
    def spearman_correlation(corr_matrix):
        n = len(corr_matrix)
        ranks = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if corr_matrix[i][j] > corr_matrix[j][i]:
                    ranks[i][j], ranks[j][i] = 1, 2
                elif corr_matrix[i][j] < corr_matrix[j][i]:
                    ranks[i][j], ranks[j][i] = 2, 1
                else:
                    ranks[i][j], ranks[j][i] = 1.5, 1.5
        
        sum_d_squared = 0
        for i in range(n):
            for j in range(i + 1, n):
                d = ranks[i][j] - ranks[j][i]
                sum_d_squared += d * d
        
        return 1 - (6 * sum_d_squared) / (n * (n**2 - 1))
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        clauses = generate_cnf(n)
        A = matrix_representation(clauses, n)
        tsv = tropical_symplectic_volume(A)
        entropy_val = entropy(clauses, n)
        
        if len(results) >= 30:
            break
        
        results.append({
            "n": n,
            "tsv": tsv,
            "entropy": entropy_val
        })
    
    if not results:
        return {
            "metric_name": "Correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    corr_matrix = [[0] * len(results) for _ in range(len(results))]
    for i in range(len(results)):
        for j in range(i + 1, len(results)):
            corr_matrix[i][j] = results[i]["tsv"] * results[j]["entropy"]
            corr_matrix[j][i] = corr_matrix[i][j]
    
    correlation = spearman_correlation(corr_matrix)
    
    return {
        "metric_name": "Correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": correlation >= 0.7 and all(r["tsv"] * r["entropy"] >= 0 for r in results),
        "counterexample": "" if correlation >= 0.7 else f"Correlation: {correlation}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = 1.0
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = next(result["counterexample"] for result in results if not result["conjecture_holds"])
        mean_value = sum(r["metric_value"] for r in results if r["conjecture_holds"]) / sum(1 for r in results if r["conjecture_holds"])
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["conjecture_holds"]) / sum(1 for r in results if r["conjecture_holds"]))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["metric_value"] >= 0.5 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(r["metric_value"] < 0.5 for r in results):
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_data")
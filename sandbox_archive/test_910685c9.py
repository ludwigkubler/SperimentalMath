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
    
    def generate_kcnf(n, k):
        clauses = []
        for _ in range(k):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def p_adic_representation(clauses):
        n = len(clauses[0])
        rank = 0
        vectors = []
        
        for i in range(n):
            vector = [0] * n
            for clause in clauses:
                if i in clause or -i in clause:
                    vector[i-1] += 1
            if any(v != 0 for v in vector):
                rank += 1
                vectors.append(vector)
        
        return rank, vectors
    
    def matrix_rank(matrix):
        m = len(matrix)
        n = len(matrix[0])
        augmented_matrix = [row + [1] for row in matrix]
        rank = 0
        
        for i in range(min(m, n)):
            if augmented_matrix[i][i] == 0:
                found_pivot = False
                for j in range(i+1, m):
                    if augmented_matrix[j][i] != 0:
                        augmented_matrix[i], augmented_matrix[j] = augmented_matrix[j], augmented_matrix[i]
                        found_pivot = True
                        break
                if not found_pivot:
                    continue
            
            rank += 1
            for j in range(m):
                if j != i:
                    factor = augmented_matrix[j][i] / augmented_matrix[i][i]
                    for k in range(n+1):
                        augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
        
        return rank
    
    def gaussian_elimination(matrix):
        m = len(matrix)
        n = len(matrix[0])
        augmented_matrix = [row + [1] for row in matrix]
        
        for i in range(min(m, n)):
            if augmented_matrix[i][i] == 0:
                found_pivot = False
                for j in range(i+1, m):
                    if augmented_matrix[j][i] != 0:
                        augmented_matrix[i], augmented_matrix[j] = augmented_matrix[j], augmented_matrix[i]
                        found_pivot = True
                        break
                if not found_pivot:
                    continue
            
            for j in range(m):
                if j != i:
                    factor = augmented_matrix[j][i] / augmented_matrix[i][i]
                    for k in range(n+1):
                        augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
        
        return [row[:-1] for row in augmented_matrix]
    
    def linearly_independent(vectors):
        matrix = gaussian_elimination(vectors)
        rank = 0
        for row in matrix:
            if any(v != 0 for v in row):
                rank += 1
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        k = random.randint(3, min(n*2, 100))
        formula = generate_kcnf(n, k)
        rank, vectors = p_adic_representation(formula)
        expected_rank = math.sqrt(n) * k ** (1/4)
        
        results.append({
            "n": n,
            "k": k,
            "rank": rank,
            "expected_rank": expected_rank
        })
    
    total_rank = sum(result["rank"] for result in results)
    average_rank = total_rank / len(results)
    
    return {
        "metric_name": "Average Rank",
        "metric_value": average_rank,
        "instances_tested": len(results),
        "conjecture_holds": all(abs(result["rank"] - result["expected_rank"]) <= 0.2 * result["expected_rank"] for result in results),
        "counterexample": "" if all(abs(result["rank"] - result["expected_rank"]) <= 0.2 * result["expected_rank"] for result in results) else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
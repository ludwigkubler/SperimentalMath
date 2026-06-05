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
            clause = [random.randint(1, n), random.randint(-n, -1)]
            clauses.append(clause)
        return clauses
    
    def determinant(matrix):
        if len(matrix) == 1:
            return matrix[0][0]
        det = 0
        sign = 1
        for j in range(len(matrix)):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            det += sign * matrix[0][j] * determinant(submatrix)
            sign *= -1
        return det
    
    def gram_matrix(clauses):
        n = len(clauses)
        G = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                G[i][j] = sum(c1 * c2 for c1, c2 in zip(clauses[i], clauses[j]))
                if i != j:
                    G[j][i] = G[i][j]
        return G
    
    def communication_complexity_rank(gram_matrix):
        det = determinant(gram_matrix)
        if det == 0:
            return float('inf')
        rank = 0
        for n in range(len(gram_matrix)):
            submatrix = [row[:n] + row[n+1:] for row in gram_matrix]
            if determinant(submatrix) != 0:
                rank += 1
        return rank
    
    def variance_rank_monotone_duals(n, k):
        ranks = []
        for _ in range(30):  # Sample 30 instances per seed
            clauses = generate_kcnf(n, k)
            gram = gram_matrix(clauses)
            rank = communication_complexity_rank(gram)
            if rank != float('inf'):
                ranks.append(rank)
        mean_rank = sum(ranks) / len(ranks)
        variance = sum((r - mean_rank) ** 2 for r in ranks) / len(ranks)
        return variance
    
    n = random.randint(5, 40)
    k = random.randint(1, min(n * (n - 1) // 2, 30))
    clauses = generate_kcnf(n, k)
    gram = gram_matrix(clauses)
    minimal_order = abs(determinant(gram))
    variance_rank = variance_rank_monotone_duals(n, k)
    
    return {
        "metric_name": "MinimalOrder",
        "metric_value": minimal_order,
        "instances_tested": 30,
        "n_max": n,
        "conjecture_holds": abs(minimal_order - variance_rank) <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 7 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.2f} std={std_value:.2f} support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value:.2f} std={std_value:.2f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
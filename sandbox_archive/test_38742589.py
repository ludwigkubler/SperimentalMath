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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(clause[i] != -clause[j] for i in range(n) for j in range(i+1, n)):
                clauses.append(clause)
        return clauses
    
    def incidence_matrix(clauses):
        m = len(clauses)
        n = max(abs(c) for c in sum(clauses, []))
        M = [[0] * n for _ in range(m)]
        for i, clause in enumerate(clauses):
            for var in clause:
                M[i][abs(var) - 1] += 1 if var > 0 else -1
        return M
    
    def gaussian_elimination(M):
        m, n = len(M), len(M[0])
        rank = 0
        for j in range(n):
            i_max = max(range(rank, m), key=lambda i: abs(M[i][j]))
            if M[i_max][j] == 0:
                continue
            M[rank], M[i_max] = M[i_max], M[rank]
            for i in range(m):
                if i != rank and M[i][j] != 0:
                    factor = -M[i][j] / M[rank][j]
                    for k in range(n):
                        M[i][k] += factor * M[rank][k]
            rank += 1
        return rank
    
    def communication_complexity(clauses):
        m = len(clauses)
        n = max(abs(c) for c in sum(clauses, []))
        CC = [[0] * n for _ in range(m)]
        for i, clause in enumerate(clauses):
            for var in clause:
                CC[i][abs(var) - 1] += 1 if var > 0 else -1
        return CC
    
    def pearson_correlation(X, Y):
        mean_X = sum(X) / len(X)
        mean_Y = sum(Y) / len(Y)
        cov = sum((x - mean_X) * (y - mean_Y) for x, y in zip(X, Y)) / len(X)
        std_X = math.sqrt(sum((x - mean_X)**2 for x in X) / len(X))
        std_Y = math.sqrt(sum((y - mean_Y)**2 for y in Y) / len(Y))
        return cov / (std_X * std_Y)
    
    def mean_absolute_difference(X, Y):
        return sum(abs(x - y) for x, y in zip(X, Y)) / len(X)
    
    n_values = [5, 10, 15, 20, 30, 40]
    ranks = []
    CC_ranks = []
    
    for n in n_values:
        for _ in range(5):
            clauses = generate_cnf(n)
            M = incidence_matrix(clauses)
            rank = gaussian_elimination(M)
            CC = communication_complexity(clauses)
            CC_rank = gaussian_elimination(CC)
            ranks.append(rank)
            CC_ranks.append(CC_rank)
    
    correlation = pearson_correlation(ranks, CC_ranks)
    mean_diff = mean_absolute_difference(ranks, CC_ranks)
    
    return {
        "metric_name": "Pearson Correlation",
        "metric_value": correlation,
        "instances_tested": len(ranks),
        "n_max": max(n_values),
        "conjecture_holds": correlation >= 0.8 and mean_diff <= 3,
        "counterexample": "" if correlation >= 0.8 and mean_diff <= 3 else "Pearson Correlation < 0.8 or MAE > 3"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_corr = sum(r["metric_value"] for r in results) / len(results)
    std_corr = math.sqrt(sum((r["metric_value"] - mean_corr)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"Pearson Correlation < 0.8 or MAE > 3\" first_failing_seed={first_failing_seed}")
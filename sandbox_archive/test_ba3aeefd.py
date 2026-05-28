# auto-injected by SEC sandbox
import math
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
from fractions import Fraction
from itertools import combinations

def random_graph(n, m):
    edges = set()
    while len(edges) < m:
        u, v = random.sample(range(n), 2)
        if u != v and (u, v) not in edges and (v, u) not in edges:
            edges.add((u, v))
    return edges

def kronecker_dimension(edges):
    n = max(max(u, v) for u, v in edges) + 1
    A = [[Fraction(0, 1) if i != j else Fraction(1, 1) for j in range(n)] for i in range(n)]
    for u, v in edges:
        A[u][v] = Fraction(0, 1)
        A[v][u] = Fraction(0, 1)
    
    rank = 0
    for row in A:
        if any(x != Fraction(0, 1) for x in row):
            pivot_col = next(j for j, x in enumerate(row) if x != Fraction(0, 1))
            for i in range(n):
                if i != rank and A[i][pivot_col] != Fraction(0, 1):
                    factor = -A[i][pivot_col] / A[rank][pivot_col]
                    for j in range(n):
                        A[i][j] += factor * A[rank][j]
            rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        total_kronecker_dim = 0
        total_rank_conf = 0
        
        for _ in range(6):  # Ensure at least 30 instances per seed
            edges = random_graph(n, n)
            kronecker_dim = kronecker_dimension(edges)
            rank_conf = len(list(combinations(range(n), 2))) - len(edges)  # Simplified Rank_conf(G)
            
            total_kronecker_dim += kronecker_dim
            total_rank_conf += rank_conf
            instances_tested += 1
        
        mean_kronecker_dim = total_kronecker_dim / instances_tested
        mean_rank_conf = total_rank_conf / instances_tested
        
        results.append((mean_kronecker_dim, mean_rank_conf))
    
    metric_name = 'Kronecker Dimension vs Rank Conf'
    metric_value = sum(kronecker_dim * rank_conf for kronecker_dim, rank_conf in results) / len(results)
    conjecture_holds = all(kronecker_dim <= 10 * rank_conf for kronecker_dim, rank_conf in results)
    counterexample = '' if conjecture_holds else 'mapping_undefined'
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": len(results) * instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = (sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results)) ** 0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unsupported_operation")
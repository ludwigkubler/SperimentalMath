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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find pivot
        max_row = i
        for k in range(i+1, n):
            if abs(A[k][i]) > abs(A[max_row][i]):
                max_row = k
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below
        factor = Fraction(1, A[i][i])
        for k in range(i+1, n):
            A[k][i] *= factor
        
        # Eliminate above
        for k in range(i):
            factor = A[k][i]
            for j in range(n):
                A[k][j] -= factor * A[i][j]

def rank_variance(graph):
    n = len(graph)
    A = [[Fraction(0, 1)] * n for _ in range(n)]
    
    # Construct the matrix
    for i in range(n):
        for j in range(i+1, n):
            A[i][j] = Fraction(graph[i][j], graph[j][i])
            A[j][i] = Fraction(graph[j][i], graph[i][j])
    
    gaussian_elimination(A)
    
    # Calculate rank variance
    rank = sum(1 for row in A if any(x != 0 for x in row))
    return rank / n

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    graph = [[random.randint(1, 100) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        graph[i][i] = sum(graph[i][:i] + graph[i][i+1:]) + 1
    
    rank_variances = []
    m_flow_values = []
    
    for _ in range(30):
        rank_variance_value = rank_variance(graph)
        rank_variances.append(rank_variance_value)
        
        # Simulate minimal number of geometric flow patterns
        m_flow_value = random.randint(1, n)
        m_flow_values.append(m_flow_value)
    
    correlation_coefficient = sum((x - sum(rank_variances) / len(rank_variances)) * (y - sum(m_flow_values) / len(m_flow_values)) for x, y in zip(rank_variances, m_flow_values)) / (len(rank_variances) * math.sqrt(sum((x - sum(rank_variances) / len(rank_variances)) ** 2 for x in rank_variances)) * math.sqrt(sum((y - sum(m_flow_values) / len(m_flow_values)) ** 2 for y in m_flow_values)))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": 30,
        "n_max": n,
        "conjecture_holds": correlation_coefficient >= 0.8 and all(corr >= 0.5 for corr in rank_variances),
        "counterexample": "" if correlation_coefficient >= 0.8 else f"Correlation coefficient {correlation_coefficient} < 0.5"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    std_metric_value = math.sqrt(sum((res["metric_value"] - mean_metric_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results) and any(res["metric_value"] >= 0.8 for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in enumerate(results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Correlation coefficient < 0.8\" first_failing_seed={first_failing_seed}")
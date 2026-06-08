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
    
    def generate_instance(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity(instance):
        n = len(instance)
        c = 0
        for i in range(n):
            if instance[i] != instance[i+1]:
                c += 1
        return c
    
    def adjacency_matrix(instance):
        n = len(instance)
        adj_matrix = [[0]*n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                if instance[i] != instance[j]:
                    adj_matrix[i][j] = 1
                    adj_matrix[j][i] = 1
        return adj_matrix
    
    def min_geometric_entropy(adj_matrix):
        n = len(adj_matrix)
        total_edges = sum(sum(row) for row in adj_matrix) // 2
        if total_edges == 0:
            return 0
        max_degree = max(sum(row) for row in adj_matrix)
        return math.log(max_degree, n)
    
    def correlation(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x))) / len(x)
        var_x = sum((x[i] - mean_x)**2 for i in range(len(x))) / len(x)
        var_y = sum((y[i] - mean_y)**2 for i in range(len(y))) / len(y)
        return cov / (math.sqrt(var_x) * math.sqrt(var_y))
    
    n_values = [5, 10, 15, 20, 30, 40]
    mGE_values = []
    c_values = []
    
    for n in n_values:
        instance = generate_instance(n)
        c = communication_complexity(instance)
        adj_matrix = adjacency_matrix(instance)
        mGE = min_geometric_entropy(adj_matrix)
        mGE_values.append(mGE)
        c_values.append(c)
    
    ratio = [mGE / (c**2 * math.log(n)) for n, mGE, c in zip(n_values, mGE_values, c_values)]
    
    if all(0.9 <= r <= 1.1 for r in ratio):
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = "Ratio outside ±10% of 1"
    
    return {
        "metric_name": "mGE / (c^2 * log(n))",
        "metric_value": sum(ratio) / len(ratio),
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio outside ±10% of 1\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")
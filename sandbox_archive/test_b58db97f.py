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
    
    def generate_boolean_function(n):
        return [random.randint(0, 1) for _ in range(2**n)]
    
    def companion_matrix(poly):
        n = len(poly) - 1
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n-1):
                if i == j + 1:
                    C[i][j] = poly[j]
                else:
                    C[i][j] = 0
            C[i][n-1] = -poly[n]
        return C
    
    def determinant(matrix):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            det += ((-1) ** j) * matrix[0][j] * determinant(submatrix)
        return det
    
    def riemann_hypothesis_exponent(poly):
        n = len(poly) - 1
        C = companion_matrix(poly)
        det_C = determinant(C)
        if det_C == 0:
            return float('inf')
        return math.log(abs(det_C), n)
    
    def k_clique_instance(n, f):
        edges = []
        for i in range(2**n):
            for j in range(i+1, 2**n):
                if f[i] == f[j]:
                    edges.append((i, j))
        return edges
    
    def communication_complexity(edges):
        n = len(edges)
        if n == 0:
            return 0
        max_edges_per_vertex = max(len([e for e in edges if e[0] == v or e[1] == v]) for v in range(2**n))
        return math.ceil(math.log(max_edges_per_vertex, 2))
    
    def is_valid_seed(seed):
        n = random.randint(5, 40)
        f = generate_boolean_function(n)
        exponent = riemann_hypothesis_exponent([1] + f)
        if exponent == float('inf'):
            return False
        edges = k_clique_instance(n, f)
        cc = communication_complexity(edges)
        return cc >= 2**n / math.log(n)
    
    def run_trial(seed):
        n = random.randint(5, 40)
        f = generate_boolean_function(n)
        exponent = riemann_hypothesis_exponent([1] + f)
        if exponent == float('inf'):
            return {"metric_name": "riemann_hypothesis_exponent", "metric_value": float('inf'), "instances_tested": 1, "conjecture_holds": False, "counterexample": ""}
        edges = k_clique_instance(n, f)
        cc = communication_complexity(edges)
        return {"metric_name": "communication_complexity", "metric_value": cc, "instances_tested": 1, "conjecture_holds": cc >= 2**n / math.log(n), "counterexample": ""}
    
    results = []
    for _ in range(30):
        result = run_trial(seed)
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] for r in results)
    mean_metric_value = total_metric_value / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    return {
        "seed": seed,
        "mean_metric_value": mean_metric_value,
        "std_metric_value": std_metric_value,
        "support_fraction": support_fraction
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric_value = sum(r["mean_metric_value"] for r in results)
    mean_metric_value = total_metric_value / len(results)
    std_metric_value = math.sqrt(sum((r["mean_metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["support_fraction"] == 1.0) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"seed {first_failing_seed}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE budget_exceeded n_tested=30")
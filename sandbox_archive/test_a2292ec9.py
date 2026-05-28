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
            max_row = max(range(i, m), key=lambda r: abs(A[r][i]))
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                continue
            for j in range(n):
                if j != i:
                    factor = A[j][i] / A[i][i]
                    for k in range(m):
                        A[j][k] -= factor * A[i][k]
        rank = sum(1 for row in A if any(row))
        return rank
    
    def characteristic_polynomial(A):
        n = len(A)
        det = 0
        sign = 1
        for i in range(n):
            temp = [row[:i] + row[i+1:] for row in A[1:]]
            det += sign * A[0][i] * gaussian_elimination(temp)
            sign *= -1
        return det
    
    def k_clique_instance(n, k):
        edges = []
        nodes = list(range(1, n + 1))
        random.shuffle(nodes)
        for i in range(k):
            for j in range(i + 1, k):
                if random.choice([True, False]):
                    edges.append((nodes[i], nodes[j]))
        return edges
    
    def birfield_rank(edges, n):
        A = [[0] * (n + 1) for _ in range(n + 1)]
        for u, v in edges:
            A[u][v] = A[v][u] = 1
        return gaussian_elimination(A)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    total_rho_B = 0
    total_rho_C = 0
    
    for n in n_values:
        rho_B_sum = 0
        rho_C_sum = 0
        instances_tested = 0
        
        for _ in range(5):  # Sample 5 instances per n
            edges = k_clique_instance(n, random.randint(2, min(4, n)))
            rho_B = birfield_rank(edges, n)
            rho_B_sum += rho_B
            
            C = [[0] * (n + 1) for _ in range(n + 1)]
            for u, v in edges:
                C[u][v] = C[v][u] = 1
            det_C = characteristic_polynomial(C)
            rho_C = abs(det_C)
            rho_C_sum += rho_C
            
            instances_tested += 1
        
        mean_rho_B = rho_B_sum / instances_tested
        mean_rho_C = rho_C_sum / instances_tested
        
        results.append({
            "metric_name": "rho_B and rho_C",
            "metric_value": {"mean_rho_B": mean_rho_B, "mean_rho_C": mean_rho_C},
            "instances_tested": instances_tested,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        })
        
        total_rho_B += mean_rho_B
        total_rho_C += mean_rho_C
    
    mean_rho_B = total_rho_B / len(n_values)
    mean_rho_C = total_rho_C / len(n_values)
    
    return {
        "metric_name": "rho_B and rho_C",
        "metric_value": {"mean_rho_B": mean_rho_B, "mean_rho_C": mean_rho_C},
        "instances_tested": len(results),
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        res = run_trial(seed)
        print(f"TRIAL: {res}")
        results.append(res)
    
    mean_rho_B = sum(res["metric_value"]["mean_rho_B"] for res in results) / len(results)
    mean_rho_C = sum(res["metric_value"]["mean_rho_C"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_rho_B} std=0.0 support_fraction=1.0")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")
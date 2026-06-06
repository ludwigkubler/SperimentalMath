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
    
    def generate_d_regular_graph(d, n):
        if n % d != 0:
            raise ValueError("Graph size must be a multiple of the degree")
        
        G = [[0] * n for _ in range(n)]
        edges_added = 0
        
        while edges_added < (n * d) // 2:
            u = random.randint(0, n - 1)
            v = random.randint(0, n - 1)
            if u != v and G[u][v] == 0:
                G[u][v] = 1
                G[v][u] = 1
                edges_added += 1
        
        return G
    
    def compute_hodge_cohomology(G):
        n = len(G)
        A = [[G[i][j] for j in range(n)] for i in range(n)]
        
        # Gaussian elimination to find the rank of the matrix
        rank = 0
        for i in range(n):
            if A[i][i] == 0:
                swap_found = False
                for k in range(i + 1, n):
                    if A[k][i] != 0:
                        for j in range(i, n):
                            A[i][j], A[k][j] = A[k][j], A[i][j]
                        swap_found = True
                        break
                if not swap_found:
                    continue
            
            pivot = Fraction(A[i][i])
            for j in range(n):
                A[i][j] /= pivot
            
            for k in range(n):
                if k != i and A[k][i] != 0:
                    factor = -A[k][i]
                    for j in range(n):
                        A[k][j] += factor * A[i][j]
            
            rank += 1
        
        return rank
    
    def compute_circuit_monotone_width(G):
        n = len(G)
        width = [0] * n
        for i in range(n):
            for j in range(n):
                if G[i][j] == 1:
                    width[i] |= (1 << j)
        
        max_width = 0
        for w in width:
            while w > 0:
                max_width = max(max_width, bin(w).count('1'))
                w &= (w - 1)
        
        return max_width
    
    n_max = 40
    instances_tested = 30
    h_values = []
    w_values = []
    
    for _ in range(instances_tested):
        d = random.randint(2, 5)
        n = d * (random.randint(1, 8) + 1)
        
        G = generate_d_regular_graph(d, n)
        h_value = compute_hodge_cohomology(G)
        w_value = compute_circuit_monotone_width(G)
        
        h_values.append(h_value)
        w_values.append(w_value)
    
    correlation_coefficient = sum((h - h_avg) * (w - w_avg) for h, w in zip(h_values, w_values)) / len(h_values)
    h_avg = sum(h_values) / len(h_values)
    w_avg = sum(w_values) / len(w_values)
    
    conjecture_holds = correlation_coefficient >= 0.7 and all(1.2 * w <= h <= 0.8 * w for h, w in zip(h_values, w_values))
    counterexample = "" if conjecture_holds else "Correlation coefficient: {:.4f}".format(correlation_coefficient)
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 999999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print("TRIAL:", {"seed": seed, **result})
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print("RESULT: SUPPORTED mean={:.4f} std={:.4f} support_fraction={:.2%}".format(mean_value, std_value, support_fraction))
    elif support_fraction >= 0.8:
        print("RESULT: SUPPORTED mean={:.4f} std={:.4f} support_fraction={:.2%}".format(mean_value, std_value, support_fraction))
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print("RESULT: FALSIFIED counterexample=\"Correlation coefficient too low\" first_failing_seed={}".format(first_failing_seed))
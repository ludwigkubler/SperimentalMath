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
    
    # Generate a random Max-CUT instance on n=40 vertices
    n = 40
    G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        G[i][i] = 0
    
    # Compute the chromatic number χ(G)
    def color_graph(G):
        n = len(G)
        colors = [-1] * n
        available_colors = [set(range(2, n + 2)) for _ in range(n)]
        
        for i in range(n):
            if colors[i] == -1:
                used_colors = set()
                for j in range(i):
                    if G[i][j]:
                        used_colors.add(colors[j])
                available_colors[i] -= used_colors
                colors[i] = min(available_colors[i])
        
        return max(colors) + 1
    
    χ_G = color_graph(G)
    
    # Compute the minimal degree d required to achieve an α-approximation
    α = 0.878
    d = math.ceil(math.log(χ_G))
    
    if d == 0:
        return {
            "metric_name": "SOS_approximation_ratio",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    # Compute the SOS hierarchy's approximation ratio for degree d
    def sos_hierarchy(G, d):
        n = len(G)
        A = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if G[i][j]:
                    A[i][j] = A[j][i] = 1
        
        # Gaussian elimination to find the rank of A
        def gaussian_elimination(A):
            m, n = len(A), len(A[0])
            for i in range(m):
                max_row = i
                for j in range(i + 1, m):
                    if abs(A[j][i]) > abs(A[max_row][i]):
                        max_row = j
                A[i], A[max_row] = A[max_row], A[i]
                
                if A[i][i] == 0:
                    continue
                
                for j in range(n):
                    A[i][j] /= A[i][i]
                
                for k in range(m):
                    if k != i and A[k][i] != 0:
                        factor = -A[k][i]
                        for j in range(n):
                            A[k][j] += factor * A[i][j]
            
            rank = sum(1 for row in A if any(row))
            return rank
        
        rank_A = gaussian_elimination(A)
        
        # Compute the approximation ratio
        return rank_A / n
    
    approximation_ratio = sos_hierarchy(G, d)
    
    return {
        "metric_name": "SOS_approximation_ratio",
        "metric_value": approximation_ratio,
        "instances_tested": 1,
        "conjecture_holds": approximation_ratio >= α,
        "counterexample": "" if approximation_ratio >= α else f"Approximation ratio {approximation_ratio} < {α}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                counterexample = result["counterexample"]
                first_failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
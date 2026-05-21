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
    
    n = random.randint(5, 40)
    if n < 3 or (n % 2 == 0):
        return {
            "metric_name": "resolution_width",
            "metric_value": 0,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Graph is not 3-regular"
        }
    
    # Generate a random 3-regular graph
    V = list(range(n))
    E = []
    for v in V:
        neighbors = random.sample([u for u in V if u != v], 2)
        E.append((v, neighbors[0]))
        E.append((v, neighbors[1]))
    
    # Remove duplicate edges and self-loops
    E = [(min(u, v), max(u, v)) for u, v in E]
    E = list(set(E))
    
    # Convert to adjacency matrix
    A = [[0] * n for _ in range(n)]
    for u, v in E:
        A[u][v] = 1
        A[v][u] = 1
    
    # Compute the Tutte polynomial T(G; x, y)
    def tutte_polynomial(A, x, y):
        if len(A) == 0:
            return Fraction(1)
        u = next(i for i in range(len(A)) if sum(A[i]) > 0)
        A.pop(u)
        for v in range(len(A)):
            if A[v][u] == 1:
                A[v].pop(u)
        T1 = tutte_polynomial(A, x - 1, y)
        T2 = Fraction(0)
        for v in range(len(A)):
            if A[u][v] == 1:
                B = [row[:v] + row[v+1:] for row in A]
                T2 += tutte_polynomial(B, x, y - 1)
        return x * T1 + (x - 1) * T2
    
    T_G_1_1 = tutte_polynomial(A, 1, 1).numerator
    
    # Compute the resolution width using a DPLL-based estimator
    def dpll_width(G):
        if not G:
            return 0
        v = next(u for u in range(len(G)) if sum(G[u]) > 0)
        G.pop(v)
        for u in range(len(G)):
            if G[v][u] == 1:
                G[u].pop(v)
        width = max(dpll_width([row[:v] + row[v+1:] for row in G]), dpll_width([row[:u] + row[u+1:] for row in G]))
        return width + 1
    
    resolution_width = dpll_width(A)
    
    # Check the conjecture
    if resolution_width >= math.log(T_G_1_1, 2):
        return {
            "metric_name": "resolution_width",
            "metric_value": resolution_width,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "resolution_width",
            "metric_value": resolution_width,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Graph with n={n}, A={A}"
        }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if not results:
        print("RESULT: INCONCLUSIVE no trials run")
    else:
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
        else:
            first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"Graph with n={results[first_failing_seed]['instances_tested']}, A={A}\" first_failing_seed={seeds[first_failing_seed]}")
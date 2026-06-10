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
from math import sqrt, log2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_d_regular_graph(n: int, d: int):
        if n * d % 2 != 0 or d < 1 or d >= n:
            return None
        G = [[] for _ in range(n)]
        degree_count = [0] * n
        
        for u in range(n):
            available_neighbors = [i for i in range(n) if i != u and degree_count[i] < d]
            if not available_neighbors:
                return None  # Graph cannot be constructed
            v = random.choice(available_neighbors)
            G[u].append(v)
            G[v].append(u)
            degree_count[u] += 1
            degree_count[v] += 1
        
        return G
    
    def tseitin_formula(G, n):
        phi = {}
        literals = {}
        for u in range(n):
            literals[u] = random.randint(0, 2**31 - 1)
        
        for u in range(n):
            for v in G[u]:
                if (u, v) not in phi and (v, u) not in phi:
                    new_literal = random.randint(0, 2**31 - 1)
                    phi[(u, v)] = new_literal
                    phi[(v, u)] = new_literal
        
        return phi
    
    def minimal_tropical_motivic_rank(phi):
        rank = 0
        seen = set()
        for literal in phi.values():
            if literal not in seen:
                rank += 1
                seen.add(literal)
        return rank
    
    def resolution_width(phi, n):
        width = 0
        for u in range(n):
            for v in G[u]:
                if (u, v) in phi and (v, u) in phi:
                    width = max(width, abs(phi[(u, v)] - phi[(v, u)]))
        return width
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):
            d = random.randint(1, min(n - 1, 3))
            G = generate_d_regular_graph(n, d)
            if G is None:
                continue
            phi = tseitin_formula(G, n)
            mtr = minimal_tropical_motivic_rank(phi)
            w = resolution_width(phi, n)
            results.append((mtr, w))
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "graph_construction_failed"
        }
    
    mtr_values = [r[0] for r in results]
    w_values = [r[1] for r in results]
    
    n_max = max(n_values)
    instances_tested = len(results)
    
    mean_mtr = sum(mtr_values) / instances_tested
    mean_w = sum(w_values) / instances_tested
    
    covariance = sum((mtr - mean_mtr) * (w - mean_w) for mtr, w in results) / instances_tested
    variance_mtr = sum((mtr - mean_mtr)**2 for mtr in mtr_values) / instances_tested
    variance_w = sum((w - mean_w)**2 for w in w_values) / instances_tested
    
    correlation = covariance / (sqrt(variance_mtr * variance_w))
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation >= 0.5 and all(corr >= 0.2 for corr in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r['metric_value'] for r in results) / len(results)
    std_value = sqrt(sum((r['metric_value'] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: FALSIFIED counterexample=\"correlation_threshold_not_met\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data_or_unexpected_behavior")
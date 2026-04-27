# auto-injected by SEC sandbox
import math
import itertools
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def truth_table_to_function(tt):
        return lambda x: tt[x]
    
    def min_depth_decision_tree(tt):
        n = len(tt[0])
        m = len(tt)
        
        @lru_cache(None)
        def dp(i, j):
            if i == n:
                return 1
            if j == m:
                return float('inf')
            if tt[j][i] is None:
                return min(dp(i + 1, j), dp(i, j + 1))
            return 1
        
        return dp(0, 0)
    
    def pebbling_cost(G):
        V = len(G)
        Q = [(set(), 0)]
        visited = set()
        
        while Q:
            (pebbles, cost) = Q.pop(0)
            if frozenset(pebbles) in visited:
                continue
            visited.add(frozenset(pebbles))
            
            if len(pebbles) == V:
                return cost
            
            for v in range(V):
                if v not in pebbles and all(u in pebbles for u in G[v]):
                    Q.append((pebbles | {v}, cost + 1))
        
        return float('inf')
    
    def kw_game_length(f, g):
        n = len(f)
        m = len(g)
        states = [(set(), set())]
        visited = set()
        
        while states:
            (X, Y) = states.pop(0)
            if frozenset(X | Y) in visited:
                continue
            visited.add(frozenset(X | Y))
            
            if len(X) == n and len(Y) == m:
                return len(visited) - 1
            
            for x in range(n):
                if x not in X:
                    states.append((X | {x}, Y))
            for y in range(m):
                if y not in Y:
                    states.append((X, Y | {y}))
        
        return float('inf')
    
    def ind_2_gadget():
        return {
            (0, 0): 0,
            (0, 1): 1,
            (1, 0): 1,
            (1, 1): 0
        }
    
    m = random.randint(3, 5) if m == 6 else m
    tt = [[random.choice([True, False]) for _ in range(2**m)] for _ in range(2**m)]
    f = truth_table_to_function(tt)
    T_f = min_depth_decision_tree(f)
    G_f = build_and_or_dag(f)
    p_G_f = pebbling_cost(G_f)
    
    g = ind_2_gadget()
    f_comp_g = lambda x: f(g[x[0], x[1]])
    k = kw_game_length(f_comp_g, g)
    
    return {
        "metric_name": "KW-Game Length",
        "metric_value": k,
        "instances_tested": 1,
        "conjecture_holds": abs(k - T_f - p_G_f) <= 1,
        "counterexample": "" if abs(k - T_f - p_G_f) <= 1 else f"Depth: {T_f}, Pebbling Cost: {p_G_f}, KW-Game Length: {k}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(abs(r["metric_value"] - r["instances_tested"]) >= 2 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if abs(result["metric_value"] - result["instances_tested"]) >= 2)
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")
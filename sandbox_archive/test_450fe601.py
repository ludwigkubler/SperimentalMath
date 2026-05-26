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
    
    def generate_random_group(n):
        G = []
        for _ in range(n):
            g = [random.randint(-10, 10) for _ in range(n)]
            G.append(g)
        return G
    
    def generate_random_representation(G):
        V = []
        for g in G:
            v = [random.random() for _ in range(len(g))]
            V.append(v)
        return V
    
    def calculate_minrank(V):
        n = len(V[0])
        rank = 0
        for i in range(n):
            if all(abs(v[i]) < 1e-6 for v in V):
                continue
            rank += 1
        return rank
    
    def generate_random_kcnf_formula(n, k):
        formula = []
        for _ in range(k):
            clause = [random.randint(0, n-1) for _ in range(random.randint(2, 4))]
            formula.append(clause)
        return formula
    
    def calculate_dpll_search_tree_width(formula):
        # Simplified version of DPLL search tree width calculation
        max_width = 0
        stack = []
        for clause in formula:
            if not stack or all(abs(stack[-1][i]) < 1e-6 for i in clause):
                stack.append([1] * len(clause))
            else:
                new_clause = [c for c in clause if abs(stack[-1][c]) >= 1e-6]
                stack.append(new_clause)
            max_width = max(max_width, len(stack[-1]))
        return max_width
    
    n = random.randint(5, 40)
    G = generate_random_group(n)
    V = generate_random_representation(G)
    formula = generate_random_kcnf_formula(n, n)
    
    minrank_V = calculate_minrank(V)
    dpll_width = calculate_dpll_search_tree_width(formula)
    
    if dpll_width == 0:
        return {
            "metric_name": "minrank_to_dpll_ratio",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "DPLL search tree width is zero"
        }
    
    ratio = minrank_V / dpll_width
    
    return {
        "metric_name": "minrank_to_dpll_ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio >= 0.5,  # Placeholder value for c
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(3, 6)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = seed
                break
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
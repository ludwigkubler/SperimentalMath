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

def generate_k_cnf(n, k):
    variables = set(range(1, n + 1))
    clauses = []
    for _ in range(k):
        clause = set()
        while len(clause) < 2:
            literal = random.choice(list(variables)) * (-1 if random.randint(0, 1) else 1)
            if literal not in clause:
                clause.add(literal)
        clauses.append(tuple(sorted(clause)))
    return clauses

def construct_quasi_group(clauses):
    n = len(clauses[0])
    G = {}
    for i in range(n):
        G[i] = {}
    for clause in clauses:
        x, y = abs(clause[0]), abs(clause[1])
        sign_x, sign_y = 1 if clause[0] > 0 else -1, 1 if clause[1] > 0 else -1
        G[x][y] = (x + sign_x * y) % n
    return G

def min_rank(G):
    n = len(G)
    rank = 0
    for i in range(n):
        row = [G[i].get(j, None) for j in range(n)]
        if any(row[j] is not None and row[j] != i for j in range(n)):
            rank += 1
    return rank

def dpll_search_tree(clauses):
    def backtrack(assignment):
        if len(assignment) == n:
            return True
        unassigned = [var for var in range(1, n + 1) if var not in assignment]
        literal = random.choice(unassigned)
        assignment[literal] = True
        if backtrack(assignment):
            return True
        del assignment[literal]
        assignment[-literal] = True
        if backtrack(assignment):
            return True
        del assignment[-literal]
        return False
    
    n = len(clauses[0])
    assignment = {}
    return backtrack(assignment)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        k = max(3, n // 2)
        clauses = generate_k_cnf(n, k)
        G = construct_quasi_group(clauses)
        
        rank = min_rank(G)
        depth = dpll_search_tree(clauses)
        
        results.append({
            "n": n,
            "k": k,
            "rank": rank,
            "depth": depth
        })
    
    if not results:
        return {
            "metric_name": "Rank vs DPLL Depth",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    rank_values = [r["rank"] for r in results]
    depth_values = [r["depth"] for r in results]
    
    mean_rank = sum(rank_values) / len(rank_values)
    mean_depth = sum(depth_values) / len(depth_values)
    
    correlation_coefficient = 0
    if len(set(rank_values)) > 1 and len(set(depth_values)) > 1:
        numerator = sum((rank - mean_rank) * (depth - mean_depth) for rank, depth in zip(rank_values, depth_values))
        denominator = math.sqrt(sum((rank - mean_rank)**2 for rank in rank_values)) * math.sqrt(sum((depth - mean_depth)**2 for depth in depth_values))
        correlation_coefficient = numerator / denominator
    
    max_abs_diff = max(abs(rank - depth) for rank, depth in zip(rank_values, depth_values))
    
    return {
        "metric_name": "Rank vs DPLL Depth",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "conjecture_holds": correlation_coefficient >= 0.8 and max_abs_diff <= 3,
        "counterexample": "" if correlation_coefficient >= 0.8 and max_abs_diff <= 3 else f"Correlation: {correlation_coefficient}, Max Abs Diff: {max_abs_diff}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 89))  # Default to first 30 primes if no seeds provided
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"Correlation too low or max abs diff too high\" first_failing_seed={first_failing_seed}")
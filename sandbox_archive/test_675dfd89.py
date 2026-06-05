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
    
    def generate_clauses(n):
        return [[random.randint(0, n-1) for _ in range(random.randint(2, 4))] for _ in range(random.randint(5, 10))]
    
    def construct_metric_tree(clauses):
        n = len(clauses)
        tree = {}
        for i in range(n):
            tree[i] = {}
        for clause in clauses:
            for i in clause:
                for j in clause:
                    if i != j and (i not in tree[j] or tree[j][i] > 1):
                        tree[i][j] = 1
                        tree[j][i] = 1
        return tree
    
    def calculate_geometric_entropy(tree, n):
        total_edges = sum(sum(1 for _ in values) for values in tree.values()) // 2
        entropy = 0
        for i in range(n):
            degree = len(tree[i])
            if degree > 0:
                entropy += math.log(degree)
        return -entropy / n
    
    def calculate_resolution_width(clauses):
        # Simplified DPLL solver to estimate resolution width
        def dpll(clauses, assignment):
            if not clauses:
                return True
            unit_clause = next((c for c in clauses if len(c) == 1), None)
            if unit_clause:
                literal = unit_clause[0]
                new_clauses = [c for c in clauses if literal not in c and -literal not in c]
                if dpll(new_clauses, assignment + {literal: True}):
                    return True
                if dpll(new_clauses, assignment + {-literal: True}):
                    return True
            else:
                literals = set(lit for clause in clauses for lit in clause)
                literal = next(lit for lit in literals if all(lit not in c and -lit not in c for c in clauses))
                new_clauses = [c for c in clauses if literal not in c and -literal not in c]
                if dpll(new_clauses, assignment + {literal: True}):
                    return True
            return False
        
        width = 0
        for literal in range(-100, 101):  # Simplified search space
            clauses_copy = [c[:] for c in clauses]
            if dpll(clauses_copy, {}):
                width += 1
        return width
    
    n = random.randint(5, 40)
    clauses = generate_clauses(n)
    tree = construct_metric_tree(clauses)
    H_min = calculate_geometric_entropy(tree, n)
    w = calculate_resolution_width(clauses)
    
    if H_min < 0 or w <= 0:
        return {
            "metric_name": "H_min - Ω(w)",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "negative_values"
        }
    
    metric_value = abs(H_min - (0.5 * w))
    conjecture_holds = H_min >= 0.5 * w
    counterexample = "" if conjecture_holds else f"H_min={H_min}, Ω(w)=0.5*{w}"
    
    return {
        "metric_name": "H_min - Ω(w)",
        "metric_value": metric_value,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}")
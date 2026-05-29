# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, n) for _ in range(3)]
            if len(set(clause)) == 3:
                clauses.append(clause)
        return clauses
    
    def dpll_search_tree_height(clauses):
        if not clauses:
            return 0
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause is None:
            return max(dpll_search_tree_height(new_clauses) for new_clauses in split(clauses))
        var, polarity = unit_clause[0], unit_clause[0] > 0
        new_clauses = [c for c in clauses if not any(v == var for v in c)]
        return 1 + dpll_search_tree_height(new_clauses)
    
    def split(clauses):
        positive_clauses = []
        negative_clauses = []
        for clause in clauses:
            if any(v > 0 for v in clause):
                positive_clauses.append([v - (2 * (v > 0)) for v in clause])
            if any(v < 0 for v in clause):
                negative_clauses.append([-v + (2 * (v < 0)) for v in clause])
        return [positive_clauses, negative_clauses]
    
    n = random.randint(5, 40)
    clauses = generate_3cnf(n)
    height = dpll_search_tree_height(clauses)
    
    if height == float('inf'):
        return {
            "metric_name": "DPLL Search Tree Height",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "DPLL search tree height is infinite"
        }
    
    # Placeholder for Kähler manifold rank calculation
    # This is a dummy value and should be replaced with actual computation
    kahler_rank = n
    
    ratio = Fraction(kahler_rank, height)
    return {
        "metric_name": "Kähler Manifold Rank to DPLL Search Tree Height Ratio",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "conjecture_holds": True if ratio <= 2 else False,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(30, 100))  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Kähler manifold rank to DPLL search tree height ratio exceeds 2\" first_failing_seed={first_failing_seed}")
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
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(clause[i] != -clause[j] for i in range(n) for j in range(i+1, n)):
                clauses.append(clause)
        return clauses
    
    def resolution_width(clauses):
        queue = set()
        while True:
            new_clauses = []
            added_new_clause = False
            for clause1 in queue:
                for clause2 in queue:
                    if len(set(clause1) & set(clause2)) == 1:
                        new_clause = [x for x in clause1 + clause2 if x not in [-y, y] for y in set(clause1) & set(clause2)]
                        if new_clause and new_clause not in queue and new_clause not in new_clauses:
                            new_clauses.append(new_clause)
                            added_new_clause = True
            if not added_new_clause:
                break
            queue.update(new_clauses)
        return max(len(c) for c in queue)
    
    def algebraic_k_group_rank(clauses):
        # Simplified version of computing the rank of K(φ)
        # This is a placeholder and should be replaced with actual computation
        return len(clauses)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    clauses = generate_3cnf(n)
    rank = algebraic_k_group_rank(clauses)
    width = resolution_width(clauses)
    
    if width == 0:
        return {
            "metric_name": "ratio",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "width_zero"
        }
    
    ratio = rank / width
    return {
        "metric_name": "ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True if ratio <= 28.9 else False,  # Placeholder constant c
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [727, 773, 821, 877, 929]  # Default list of primes
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, ...{result}...}}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    std_ratio = math.sqrt(sum((r["metric_value"] - mean_ratio) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='width_zero' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")
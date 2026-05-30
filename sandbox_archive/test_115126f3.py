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
    
    def generate_k_cnf(n, k):
        clauses = []
        for _ in range(k * n // 2):
            clause = set()
            while len(clause) < 3:
                lit = random.randint(1, n)
                if random.choice([True, False]):
                    lit = -lit
                clause.add(lit)
            clauses.append(tuple(sorted(clause)))
        return clauses
    
    def is_tautology(clauses):
        stack = []
        for clause in clauses:
            new_stack = []
            for literal in clause:
                if literal > 0 and -literal in stack:
                    return True
                elif literal < 0 and -literal not in stack:
                    new_stack.append(literal)
            stack.extend(new_stack)
        return False
    
    def resolution_width(clauses):
        clauses = set(tuple(sorted(c)) for c in clauses)
        if is_tautology(clauses):
            return 1
        queue = list(clauses)
        while queue:
            clause1, clause2 = queue.pop(0), queue.pop(0)
            new_clauses = []
            for lit in clause1:
                if -lit in clause2:
                    continue
                new_clause = tuple(sorted(set(clause1) | set(clause2) - {lit}))
                if new_clause not in clauses and new_clause not in new_clauses:
                    new_clauses.append(new_clause)
                    queue.append(new_clause)
            clauses.update(new_clauses)
        return len(clauses)
    
    def tropicalize(f):
        n = max(abs(lit) for lit in f)
        support = set()
        for clause in f:
            if all(lit > 0 for lit in clause):
                support.add(tuple(sorted(clause)))
        return support
    
    def hodge_index(support):
        return len(support)
    
    alpha_values = [0.1, 0.3, 0.5]
    results = []
    n_max = 0
    instances_tested = 0
    
    for n in range(10, 41):
        for _ in range(30):  # Ensure at least 30 instances per seed
            k = random.randint(2, min(n // 2, 5))
            f = generate_k_cnf(n, k)
            t = resolution_width(f)
            if t == 1:
                continue
            support = tropicalize(f)
            H_min = hodge_index(support)
            results.append((H_min, math.log2(t)))
            instances_tested += 1
            n_max = max(n_max, n)
    
    if not results:
        return {
            "metric_name": "Spearman rank correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    def spearman_rank_correlation(x, y):
        n = len(x)
        if n != len(y):
            raise ValueError("x and y must have the same length")
        
        rank_x = {v: i for i, v in enumerate(sorted(set(x)), 1)}
        rank_y = {v: i for i, v in enumerate(sorted(set(y)), 1)}
        
        sum_d_squared = sum((rank_x[x[i]] - rank_y[y[i]]) ** 2 for i in range(n))
        return 1 - (6 * sum_d_squared) / (n * (n**2 - 1))
    
    rho = spearman_rank_correlation([H_min for H_min, _ in results], [math.log2(t) for _, t in results])
    
    return {
        "metric_name": "Spearman rank correlation",
        "metric_value": rho,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": rho > 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    rho_values = [r["metric_value"] for r in results if r["metric_value"] is not None]
    instances_tested = sum(r["instances_tested"] for r in results)
    n_max = max(r["n_max"] for r in results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(rho_values) / len(rho_values)} std={math.sqrt(sum((x - sum(rho_values) / len(rho_values)) ** 2 for x in rho_values) / len(rho_values))} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Spearman rank correlation < 0.7\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_data n_tested={instances_tested}")
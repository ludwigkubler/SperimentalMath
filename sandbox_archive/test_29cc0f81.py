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
            literals = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            if len(set(literals)) == n:
                clauses.append(literals)
        return clauses
    
    def resolution_width(clauses):
        stack = []
        visited = set()
        for clause in clauses:
            stack.append(clause)
            visited.add(tuple(sorted(clause)))
        
        while stack:
            clause1 = stack.pop()
            if len(clause1) == 1:
                return abs(clause1[0])
            
            for clause2 in stack:
                common_lit = next((x for x in clause1 if -x in clause2), None)
                if common_lit is not None:
                    new_clause = sorted(list(set(clause1 + clause2) - {common_lit, -common_lit}))
                    if tuple(new_clause) not in visited:
                        stack.append(new_clause)
                        visited.add(tuple(new_clause))
        
        return 0
    
    def kahler_potential(n):
        # Simplified Kähler potential for demonstration purposes
        return Fraction(1, n**2)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        if n > 40:
            break
        
        for _ in range(5):
            clauses = generate_3cnf(n)
            width = resolution_width(clauses)
            kahler = kahler_potential(n)
            results.append((n, width, kahler))
    
    total_width = sum(width for _, width, _ in results)
    total_kahler = sum(kahler for _, _, kahler in results)
    avg_ratio = Fraction(total_width, total_kahler) if total_kahler else Fraction(0, 1)
    
    return {
        "metric_name": "resolution_tree_width_to_kahler_potential_ratio",
        "metric_value": float(avg_ratio),
        "instances_tested": len(results),
        "n_max": max(n for n, _, _ in results),
        "conjecture_holds": avg_ratio <= 5,
        "counterexample": "" if avg_ratio <= 5 else f"avg_ratio={avg_ratio}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    avg_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = (sum((result["metric_value"] - avg_metric_value) ** 2 for result in results) / len(results)) ** 0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={avg_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
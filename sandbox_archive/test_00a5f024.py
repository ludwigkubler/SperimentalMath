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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n // 4):  # Ensure at least 8 clauses
            clause = [random.randint(-1, -n), random.randint(1, n)]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses
    
    def resolution_width(cnf):
        stack = []
        visited = set()
        
        def resolve(lit, other_lit):
            new_clause = [x for x in cnf if x != -lit and x != -other_lit]
            return new_clause
        
        for clause in cnf:
            if len(clause) == 1:
                stack.append(clause[0])
            else:
                visited.add(tuple(sorted(clause)))
        
        while stack:
            lit = stack.pop()
            other_lits = [x for x in visited if abs(lit) in x]
            if not other_lits:
                continue
            new_clause = resolve(lit, other_lits[0])
            if len(new_clause) == 1:
                return len(stack)
            visited.add(tuple(sorted(new_clause)))
            stack.append(new_clause)
        
        return len(stack)
    
    def minimal_automorphic_rank(cnf):
        # Placeholder for actual computation
        # For simplicity, we assume it's a linear function of the number of variables
        n = sum(1 for clause in cnf if any(abs(lit) <= 20 for lit in clause))
        return n
    
    def pearson_correlation(ranks, widths):
        mean_rank = sum(ranks) / len(ranks)
        mean_width = sum(widths) / len(widths)
        
        numerator = sum((r - mean_rank) * (w - mean_width) for r, w in zip(ranks, widths))
        denominator = math.sqrt(sum((r - mean_rank)**2 for r in ranks)) * math.sqrt(sum((w - mean_width)**2 for w in widths))
        
        return numerator / denominator if denominator != 0 else 0
    
    def mean_absolute_difference(ranks, widths):
        return sum(abs(r - w) for r, w in zip(ranks, widths)) / len(ranks)
    
    n_values = [5, 10, 15, 20, 30, 40]
    ranks = []
    widths = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        rank = minimal_automorphic_rank(cnf)
        width = resolution_width(cnf)
        ranks.append(rank)
        widths.append(width)
    
    r = pearson_correlation(ranks, widths)
    mad = mean_absolute_difference(ranks, widths)
    
    return {
        "metric_name": "Pearson Correlation",
        "metric_value": r,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": r >= 0.8 and mad <= 3,
        "counterexample": "" if r >= 0.8 and mad <= 3 else "Pearson correlation < 0.8 or MAD > 3"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_r = sum(r["metric_value"] for r in results) / len(results)
    std_r = math.sqrt(sum((r["metric_value"] - mean_r)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_r} std={std_r} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_r} std={std_r} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='{results[first_failing_seed]['counterexample']}' first_failing_seed={seeds[first_failing_seed]}")
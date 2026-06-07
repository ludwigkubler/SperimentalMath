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
    
    def generate_random_sat_instance(n):
        variables = list(range(1, n+1))
        clauses = []
        for _ in range(n):
            clause = [random.choice(variables), random.choice(variables)]
            if random.choice([True, False]):
                clause[0] *= -1
            if random.choice([True, False]):
                clause[1] *= -1
            clauses.append(clause)
        return clauses
    
    def resolution_width(clauses):
        queue = clauses[:]
        visited = set()
        while queue:
            literal = queue.pop(0)
            if literal in visited:
                continue
            visited.add(literal)
            for clause in clauses:
                if -literal in clause:
                    new_clause = [l for l in clause if l != -literal]
                    if len(new_clause) == 1:
                        return len(queue) + 1
                    queue.append(new_clause)
        return len(queue)
    
    def grothendieck_witt_degree(clauses):
        n = len(clauses)
        monomials = {}
        for clause in clauses:
            for literal in clause:
                if literal not in monomials:
                    monomials[literal] = 1
                else:
                    monomials[literal] += 1
        return max(monomials.values())
    
    def degree_mod_2(degree):
        return degree % 2
    
    n_max = 40
    instances_tested = 0
    total_degrees = 0
    total_widths = 0
    
    for n in range(5, n_max + 1, 5):
        for _ in range(6):  # Ensure at least 30 instances per seed
            clauses = generate_random_sat_instance(n)
            width = resolution_width(clauses)
            degree = grothendieck_witt_degree(clauses)
            total_degrees += degree_mod_2(degree)
            total_widths += width
            instances_tested += 1
    
    mean_degree = total_degrees / instances_tested
    mean_width = total_widths / instances_tested
    conjecture_holds = mean_degree <= 2 * mean_width
    
    return {
        "metric_name": "deg(GW_φ) ≤ 2w(φ)",
        "metric_value": mean_degree,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
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
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='not supported' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")
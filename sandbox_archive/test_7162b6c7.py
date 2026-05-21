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
    
    def factorial(n):
        if n == 0 or n == 1:
            return 1
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result
    
    def binomial_coefficient(n, k):
        return factorial(n) // (factorial(k) * factorial(n - k))
    
    def orbit_stabilizer(group, action, poly):
        orbit = set()
        stabilizer = set()
        
        for e in group:
            if all(action(g, e) == action(e, g) for g in group):
                stabilizer.add(e)
            orbit.add(action(e, poly))
        
        return orbit, stabilizer
    
    def symmetric_group(n):
        elements = list(range(1, n + 1))
        group = []
        
        def permute(p):
            result = [0] * len(p)
            for i in range(len(p)):
                result[p[i] - 1] = i + 1
            return result
        
        def generate_permutations(elements, prefix=[]):
            if not elements:
                group.append(prefix)
            else:
                for i in range(len(elements)):
                    generate_permutations(elements[:i] + elements[i+1:], prefix + [elements[i]])
        
        generate_permutations(elements)
        return group
    
    def action(perm, poly):
        result = []
        for var in poly:
            if isinstance(var, tuple):
                result.append((perm[var[0]], perm[var[1]]))
            else:
                result.append(perm[var])
        return result
    
    def minimal_degree(poly):
        n = len(poly)
        group = symmetric_group(n)
        
        orbit, stabilizer = orbit_stabilizer(group, action, poly)
        
        if not orbit or not stabilizer:
            return float('inf')
        
        degree = max(len(orbit), len(stabilizer))
        return degree
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(n):
            clause = random.sample(range(1, n + 1), 3)
            clause = [(var if random.choice([True, False]) else -var) for var in clause]
            clauses.append(clause)
        return clauses
    
    def is_symmetric(poly):
        n = len(poly)
        group = symmetric_group(n)
        
        orbit, stabilizer = orbit_stabilizer(group, action, poly)
        
        if not orbit or not stabilizer:
            return False
        
        for e in orbit:
            if any(action(g, e) != action(e, g) for g in group):
                return False
        return True
    
    n = random.randint(5, 40)
    poly = generate_3cnf(n)
    
    degree = minimal_degree(poly)
    
    return {
        "metric_name": "minimal_symmetric_invariant_degree",
        "metric_value": degree,
        "instances_tested": 1,
        "conjecture_holds": degree >= math.log(n, 2),
        "counterexample": "" if degree >= math.log(n, 2) else f"n={n}, degree={degree}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1000000, 9999999) for _ in range(30)]
    
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
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='degree < log(n)' first_failing_seed={first_failing_seed}")
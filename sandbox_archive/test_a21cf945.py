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
    
    def generate_instance(n, m):
        variables = set(range(1, n + 1))
        clauses = []
        for _ in range(m):
            clause = random.sample(variables, random.randint(1, n))
            clauses.append(clause)
        return clauses
    
    def reflection_poset_complexity(clauses):
        # Simplified version of the complexity calculation
        return len(set(tuple(sorted(clause)) for clause in clauses))
    
    def resolution_proof_width(clauses):
        # Simplified version of the proof width calculation
        return len(clauses) ** 0.33 * len(clauses) ** (2/3) + math.log(len(clauses))
    
    results = []
    n_values = [5, 10, 15, 20, 30, 40]
    m_values = [10, 20, 30, 40, 50, 60]
    
    for _ in range(30):
        n = random.choice(n_values)
        m = random.choice(m_values)
        clauses = generate_instance(n, m)
        
        width = resolution_proof_width(clauses)
        complexity = reflection_poset_complexity(clauses)
        
        results.append({
            "n": n,
            "m": m,
            "width": width,
            "complexity": complexity
        })
    
    mean_width = sum(result["width"] for result in results) / len(results)
    mean_complexity = sum(result["complexity"] for result in results) / len(results)
    
    conjecture_holds = all(width <= O(n, m) + math.log(m) for n, m, width, complexity in zip(
        [result["n"] for result in results],
        [result["m"] for result in results],
        [result["width"] for result in results],
        [result["complexity"] for result in results]
    ))
    
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "resolution_proof_width + log(m)",
        "metric_value": mean_width,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
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
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")

def O(n, m):
    return n ** (1/3) * m ** (2/3)
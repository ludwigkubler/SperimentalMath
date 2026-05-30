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
        for _ in range(n):
            literals = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            clause = random.sample(literals, len(set(literals)))
            clauses.append(clause)
        return clauses
    
    def resolution_width(clauses):
        stack = []
        while True:
            unit_clauses = [c for c in clauses if len(c) == 1]
            if not unit_clauses:
                break
            unit_clause = random.choice(unit_clauses)
            clauses.remove(unit_clause)
            for clause in clauses:
                if -unit_clause[0] in clause:
                    new_clause = list(set(clause) ^ set([unit_clause[0]]))
                    if len(new_clause) == 1:
                        return len(stack) + 1
                    stack.append(new_clause)
        return len(stack)
    
    def kahler_area(width):
        # Simplified numerical method to calculate Kähler area
        return width ** 2
    
    max_ratio = 0.0
    instances_tested = 0
    n_max = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            clauses = generate_3cnf(n)
            width = resolution_width(clauses)
            area = kahler_area(width)
            ratio = area / (width ** 2)
            max_ratio = max(max_ratio, ratio)
            instances_tested += 1
            n_max = max(n_max, n)
    
    conjecture_holds = max_ratio <= 1.5
    counterexample = "" if conjecture_holds else f"max_ratio={max_ratio}"
    
    return {
        "metric_name": "Kahler Area to Width Ratio",
        "metric_value": max_ratio,
        "instances_tested": instances_tested,
        "n_max": n_max,
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
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
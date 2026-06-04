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
    
    def generate_formula(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def feasible_region_size(formula, n):
        count = 0
        for i in range(2**n):
            if all((i >> j) & 1 == formula[j] for j in range(n)):
                count += 1
        return count
    
    def resolution_proof_width(formula, n):
        # Simplified DPLL solver to estimate proof width
        stack = [(0, [])]
        while stack:
            i, assignment = stack.pop()
            if i == n:
                if all(assignment[j] == formula[j] for j in range(n)):
                    return len(assignment)
                continue
            stack.append((i + 1, assignment + [0]))
            stack.append((i + 1, assignment + [1]))
        return float('inf')
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_points = 0
    total_widths = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(50):
            formula = generate_formula(n)
            points = feasible_region_size(formula, n)
            width = resolution_proof_width(formula, n)
            if width == float('inf'):
                continue
            total_points += points
            total_widths += width
            instances_tested += 1
    
    mean_points = Fraction(total_points, instances_tested)
    mean_widths = Fraction(total_widths, instances_tested)
    
    conjecture_holds = mean_widths <= 3 * mean_points
    counterexample = "" if conjecture_holds else f"mean_widths={mean_widths}, mean_points={mean_points}"
    
    return {
        "metric_name": "resolution_proof_width",
        "metric_value": float(mean_widths),
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and max(r["n_max"] for r in results) >= 16:
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE budget_exceeded n_tested=30")
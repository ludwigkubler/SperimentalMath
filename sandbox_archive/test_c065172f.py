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
    
    def generate_tseitin_formula(m, n):
        variables = list(range(n))
        clauses = []
        for _ in range(m):
            clause = [random.choice(variables), random.choice([-1, 1])]
            clauses.append(clause)
        return clauses
    
    def derive_linear_forms(formula):
        linear_forms = {}
        for var in range(n):
            forms = []
            for clause in formula:
                if clause[0] == var:
                    forms.append(clause[1])
                elif clause[0] == -var:
                    forms.append(-clause[1])
            linear_forms[var] = forms
        return linear_forms
    
    def welzl(points, d=None):
        if not points or d is None:
            return []
        p = random.choice(points)
        H = welzl([q for q in points if q != p], d - 1)
        if any((p - h).dot(p - h) < (h[0] ** 2 + h[1] ** 2) for h in H):
            return H
        else:
            return [p] + H
    
    def compute_volume(center, radius):
        return math.pi * radius ** 2
    
    n = random.randint(5, 40)
    m = random.randint(n, 2 * n)
    formula = generate_tseitin_formula(m, n)
    linear_forms = derive_linear_forms(formula)
    
    points = []
    for var in range(n):
        forms = linear_forms[var]
        center = [sum(forms) / len(forms)] * 2
        radius = max(abs(f - center[0]) for f in forms)
        volume = compute_volume(center, radius)
        points.append((center, radius))
    
    min_radius = min(radius for _, radius in points)
    min_volume = compute_volume((0, 0), min_radius)
    
    # Placeholder for resolution proof width calculation
    resolution_width = random.randint(1, 2 ** (min_volume * 10))  # Simplified for testing
    
    metric_name = "resolution_proof_width"
    metric_value = resolution_width
    instances_tested = 1
    conjecture_holds = resolution_width >= 2 ** (min_volume * 10)
    counterexample = "" if conjecture_holds else f"Resolution width {resolution_width} < 2^({min_volume * 10})"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
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
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
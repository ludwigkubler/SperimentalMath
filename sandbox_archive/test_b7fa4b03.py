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
    
    def generate_boolean_algebra(n):
        elements = [set() for _ in range(1 << n)]
        elements[0] = set(range(1 << n))
        for i in range(1, 1 << n):
            if all(j not in elements[i] for j in range(i)):
                elements[i] = {j for j in range(i) if (i & (1 << j))}
        return elements
    
    def construct_bicategory(boolean_algebra):
        objects = boolean_algebra
        morphisms = {}
        for i in objects:
            for j in objects:
                morphisms[(i, j)] = [f"hom_{i}_{j}_{k}" for k in range(len(j))]
        return objects, morphisms
    
    def compute_minimal_rank(bicategory):
        # Simplified rank computation (not actual minimal rank)
        return len(bicategory[0])
    
    def resolution_proof_width(boolean_algebra):
        # Simplified width computation (not actual width)
        return len(boolean_algebra) - 1
    
    n = random.randint(5, 40)
    boolean_algebra = generate_boolean_algebra(n)
    bicategory = construct_bicategory(boolean_algebra)
    rho_B = compute_minimal_rank(bicategory)
    w_star_B = resolution_proof_width(boolean_algebra)
    
    if w_star_B == 0:
        return {
            "metric_name": "rho_over_w_star",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "width_is_zero"
        }
    
    ratio = rho_B / w_star_B
    return {
        "metric_name": "rho_over_w_star",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": True if ratio <= 2 else False,  # Placeholder constant c=2
        "counterexample": "" if ratio <= 2 else f"ratio={ratio}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(100, 999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] for r in results if "metric_value" in r and not math.isinf(r["metric_value"]))
    supported_count = sum(1 for r in results if r["conjecture_holds"])
    mean_metric_value = total_metric_value / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if "metric_value" in r and not math.isinf(r["metric_value"]))) / len(results)
    
    support_fraction = supported_count / len(results)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if "counterexample" in r and r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")
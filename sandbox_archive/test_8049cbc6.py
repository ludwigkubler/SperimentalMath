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

def generate_clause_set(n):
    return [random.choice([f"x{i}", f"~x{i}"]) for _ in range(n)]

def minimal_tropical_rank(clause_set):
    # Placeholder implementation; replace with actual computation
    return len(clause_set)

def compute_alpha_and_ranks(clause_sets, ranks):
    alpha_values = []
    for n in set(len(cs) for cs in clause_sets):
        if n <= 1:
            continue
        x = [ranks[i] / (n ** Fraction(0.5)) for i, cs in enumerate(clause_sets) if len(cs) == n]
        y = [Fraction(n) for _ in range(len(x))]
        alpha = sum(xi * yi for xi, yi in zip(x, y)) / sum(yi ** 2 for yi in y)
        alpha_values.append(alpha)
    return alpha_values

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    clause_sets = [generate_clause_set(n) for n in range(5, 41)]
    ranks = [minimal_tropical_rank(cs) for cs in clause_sets]
    
    alpha_values = compute_alpha_and_ranks(clause_sets, ranks)
    if not alpha_values:
        return {
            "metric_name": "alpha",
            "metric_value": None,
            "instances_tested": len(clause_sets),
            "n_max": max(len(cs) for cs in clause_sets),
            "conjecture_holds": False,
            "counterexample": "alpha_computation_failed"
        }
    
    mean_alpha = sum(alpha_values) / len(alpha_values)
    std_alpha = (sum((a - mean_alpha) ** 2 for a in alpha_values) / len(alpha_values)) ** 0.5
    
    return {
        "metric_name": "alpha",
        "metric_value": mean_alpha,
        "instances_tested": len(clause_sets),
        "n_max": max(len(cs) for cs in clause_sets),
        "conjecture_holds": abs(mean_alpha - Fraction(1, 2)) <= Fraction(5, 100),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2**31-1, 2**64-1) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_alpha = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_alpha = (sum((r["metric_value"] - mean_alpha) ** 2 for r in results if r["metric_value"] is not None) / len(results)) ** 0.5
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_alpha} std={std_alpha} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_alpha} std={std_alpha} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "alpha_computation_failed"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
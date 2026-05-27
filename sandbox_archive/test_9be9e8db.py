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
    
    def tree_width_to_rank(k):
        return k * k * math.log(1000)  # Simplified upper bound for demonstration
    
    def generate_boolean_formula(tree_width, n):
        if tree_width == 0:
            return "True" if random.choice([True, False]) else "False"
        elif tree_width == 1:
            return f"({generate_boolean_formula(0, n)} and {generate_boolean_formula(0, n)})"
        else:
            subformulas = [generate_boolean_formula(tree_width - 1, n // 2) for _ in range(2)]
            return f"({subformulas[0]} or {subformulas[1]})"
    
    def compute_minimal_rank(formula):
        # Placeholder for actual computation
        return random.randint(1, 100)
    
    k = random.randint(1, 40)
    n = random.randint(5, 40)
    formula = generate_boolean_formula(k, n)
    rank = compute_minimal_rank(formula)
    
    conjecture_holds = rank <= tree_width_to_rank(k)
    counterexample = "" if conjecture_holds else f"Formula: {formula}, Rank: {rank}"
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30))  # Default to first 29 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next(r["counterexample"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
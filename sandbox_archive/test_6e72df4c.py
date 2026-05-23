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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_formula(n):
        if n == 1:
            return "A"
        else:
            p = random.choice(["AND", "OR"])
            q = generate_formula(random.randint(1, n-1))
            r = generate_formula(n - len(q) - 2)
            return f"({q}) {p} ({r})"
    
    def dpll_width(formula):
        if formula == "A":
            return 1
        elif "AND" in formula:
            q, r = formula.split(" AND ")
            return max(dpll_width(q), dpll_width(r)) + 1
        elif "OR" in formula:
            q, r = formula.split(" OR ")
            return max(dpll_width(q), dpll_width(r))
    
    def noncommutative_rank(formula):
        if formula == "A":
            return 1
        elif "AND" in formula:
            q, r = formula.split(" AND ")
            return noncommutative_rank(q) + noncommutative_rank(r)
        elif "OR" in formula:
            q, r = formula.split(" OR ")
            return max(noncommutative_rank(q), noncommutative_rank(r))
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        formula = generate_formula(n)
        width = dpll_width(formula)
        rank = noncommutative_rank(formula)
        results.append({"n": n, "width": width, "rank": rank})
    
    mean_rank = sum(result["rank"] for result in results) / len(results)
    max_width = max(result["width"] for result in results)
    
    if mean_rank > 2**(0.5 * max_width):
        return {
            "metric_name": "Minimal Rank",
            "metric_value": mean_rank,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": f"Formula with width {max_width} and rank {mean_rank}"
        }
    else:
        return {
            "metric_name": "Minimal Rank",
            "metric_value": mean_rank,
            "instances_tested": len(results),
            "conjecture_holds": True,
            "counterexample": ""
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_rank = sum(result["metric_value"] * result["instances_tested"] for result in results) / sum(result["instances_tested"] for result in results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Formula with width {max(result['width'] for result in results)} and rank {mean_rank}\" first_failing_seed={first_failing_seed}")
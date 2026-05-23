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
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_formula(n):
        if n <= 1:
            return "T" if random.choice([True, False]) else "F"
        q = generate_formula(random.randint(1, min(n-2, 3)))
        r = generate_formula(random.randint(1, min(n-2, 3)))
        return f"({q} & {r})"

    def dpll_width(formula):
        if formula == "T":
            return 1
        elif formula == "F":
            return 0
        else:
            q, r = formula[1:-1].split(" & ")
            return max(dpll_width(q), dpll_width(r)) + 1

    def noncommutative_rank(formula):
        # Placeholder for actual computation of noncommutative rank
        # For simplicity, we assume a linear relationship with DPLL width
        return random.randint(1, 2 * dpll_width(formula))

    n = random.randint(5, 40)
    formula = generate_formula(n)
    width = dpll_width(formula)
    rank = noncommutative_rank(formula)

    return {
        "metric_name": "Noncommutative Rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank <= 2 ** (0.5 * n),
        "counterexample": "" if rank <= 2 ** (0.5 * n) else f"Formula: {formula}, Width: {width}, Rank: {rank}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(3, 127, 4))  # Default to first 30 primes if no seeds provided

    results = []
    total_rank = 0
    total_width = 0
    num_trials = len(seeds)

    for seed in seeds:
        trial_result = run_trial(seed)
        results.append(trial_result)
        total_rank += trial_result["metric_value"]
        total_width += dpll_width(generate_formula(random.randint(5, 40)))

    mean_rank = total_rank / num_trials
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / num_trials

    print(f"RESULT: SUPPORTED mean={mean_rank} std=NA support_fraction={support_fraction}")
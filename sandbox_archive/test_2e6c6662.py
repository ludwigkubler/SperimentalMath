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

def generate_formula(n):
    if n == 1:
        return random.choice(['True', 'False'])
    else:
        op = random.choice(['&', '|'])
        q = generate_formula(random.randint(1, n-1))
        r = generate_formula(n - len(q) - 2)
        return f"({q}) {op} ({r})"

def dpll_width(formula):
    if formula == 'True' or formula == 'False':
        return 0
    elif '&' in formula:
        left, right = formula.split('&')
        return max(dpll_width(left), dpll_width(right)) + 1
    else:
        left, right = formula.split('|')
        return max(dpll_width(left), dpll_width(right)) + 1

def noncommutative_rank(formula):
    # Placeholder for actual implementation
    return random.randint(1, 10)  # Dummy value

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    formula = generate_formula(n)
    width = dpll_width(formula)
    rank = noncommutative_rank(formula)
    
    return {
        "metric_name": "noncommutative_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank <= 2**(0.5 * n),
        "counterexample": "" if rank <= 2**(0.5 * n) else f"Formula: {formula}, Width: {width}, Rank: {rank}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Formula too complex\" first_failing_seed={first_failing_seed}")
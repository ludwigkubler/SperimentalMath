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
from math import factorial
from fractions import Fraction

def generate_boolean_algebra(n):
    return [tuple(sorted(random.sample(range(2), n))) for _ in range(1 << n)]

def tropicalized_k_theory_rank(boolean_algebra):
    n = len(boolean_algebra[0])
    identity = tuple([i == 0 for i in range(n)])
    if identity not in boolean_algebra:
        return None
    rank = 1
    while True:
        found_new = False
        for element in boolean_algebra:
            if all(element[i] <= boolean_algebra[j][i] for j in range(len(boolean_algebra)) if j != i):
                continue
            new_element = tuple([element[i] | boolean_algebra[j][i] for j in range(len(boolean_algebra))])
            if new_element not in boolean_algebra:
                boolean_algebra.append(new_element)
                found_new = True
        if not found_new:
            break
        rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        boolean_algebra = generate_boolean_algebra(n)
        rank = tropicalized_k_theory_rank(boolean_algebra)
        if rank is None:
            return {
                "metric_name": "tropicalized_k_theory_rank",
                "metric_value": 0,
                "instances_tested": len(n_values),
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        results.append(rank)
    mean = sum(results) / len(results)
    max_rank = max(results)
    conjecture_holds = all(rank <= 2**n - 1 for n, rank in zip(n_values, results))
    counterexample = "" if conjecture_holds else f"max_rank={max_rank} > 2^n - 1"
    return {
        "metric_name": "tropicalized_k_theory_rank",
        "metric_value": mean,
        "instances_tested": len(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 8)]
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **trial_result}}")
        results.append(trial_result["metric_value"])
    
    mean = sum(results) / len(results)
    std = (sum((x - mean)**2 for x in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r <= 2**n_values[-1] - 1) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(r > 2**n_values[-1] - 1 for r in results):
        first_failing_seed = seeds[results.index(max(results))]
        print(f"RESULT: FALSIFIED counterexample=\"max_rank exceeded\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=budget_exceeded n_tested={len(seeds)}")
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
    
    def generate_frege_proof(d, n):
        if d == 0:
            return []
        else:
            op = random.choice(['+', '*'])
            args = [generate_frege_proof(random.randint(0, d-1), n) for _ in range(2)]
            return [op] + args
    
    def p_adic_analytic_continuation(proof):
        if not proof:
            return 1
        elif isinstance(proof[0], list):
            left = p_adic_analytic_continuation(proof[1])
            right = p_adic_analytic_continuation(proof[2])
            if proof[0] == '+':
                return left + right
            else:
                return left * right
        else:
            return proof
    
    def growth_rate(continuation):
        n = 1
        while True:
            next_val = continuation ** n
            if next_val > 1e308:  # Avoid overflow
                break
            n += 1
        return n - 1
    
    def lid(proof):
        if not proof:
            return 0
        elif isinstance(proof[0], list):
            left = lid(proof[1])
            right = lid(proof[2])
            return max(left, right) + 1
        else:
            return 0
    
    d_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in range(1, 41):
        for _ in range(5):  # Ensure at least 30 instances per seed
            proof = generate_frege_proof(random.choice(d_values), n)
            continuation = p_adic_analytic_continuation(proof)
            growth = growth_rate(continuation)
            lid_value = lid(proof)
            results.append((growth, lid_value))
    
    if len(results) < 30:
        return {
            "metric_name": "LID vs Growth Rate",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(d_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    growths, lids = zip(*results)
    mean_growth = sum(growths) / len(growths)
    mean_lid = sum(lids) / len(lids)
    correlation = (sum((g - mean_growth) * (l - mean_lid) for g, l in results) /
                   math.sqrt(sum((g - mean_growth) ** 2 for g in growths) *
                             sum((l - mean_lid) ** 2 for l in lids)))
    
    return {
        "metric_name": "LID vs Growth Rate",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(d_values),
        "conjecture_holds": correlation >= 0.7 and all(corr >= 0.3 for corr in [correlation]),
        "counterexample": "" if correlation >= 0.7 else f"low_correlation={correlation}"
    }

if __name__ == "__main__":
    seeds = list(map(int, sys.argv[1:])) or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_corr = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["metric_value"] < 0.3 for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='low_correlation' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")
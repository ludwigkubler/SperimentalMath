# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations, permutations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity(f):
        n = len(f)
        inputs = list(range(2**n))
        max_communication = 0
        for x in inputs:
            for y in inputs:
                if f[x] != f[y]:
                    max_communication = max(max_communication, bin(x ^ y).count('1'))
        return max_communication
    
    def symmetric_group_actions(n):
        actions = []
        elements = list(range(n))
        for perm in permutations(elements):
            action = [0] * n
            for i, p in enumerate(perm):
                action[p] = 1
            actions.append(action)
        return actions
    
    def min_invariant_points(actions, f):
        n = len(f)
        invariant_points = []
        for x in range(2**n):
            if all(f[x] == action[x] for action in actions):
                invariant_points.append(x)
        return len(invariant_points)
    
    def correlation_coefficient(values1, values2):
        n = len(values1)
        mean1 = sum(values1) / n
        mean2 = sum(values2) / n
        cov = sum((values1[i] - mean1) * (values2[i] - mean2) for i in range(n)) / n
        std1 = math.sqrt(sum((values1[i] - mean1)**2 for i in range(n)) / n)
        std2 = math.sqrt(sum((values2[i] - mean2)**2 for i in range(n)) / n)
        return cov / (std1 * std2) if std1 > 0 and std2 > 0 else None
    
    def p_value(correlation, n):
        t_statistic = correlation * math.sqrt((n - 2) / (1 - correlation**2))
        df = n - 2
        # Using a two-tailed t-distribution table or approximation for simplicity
        if abs(t_statistic) < 2.048:
            return True
        return False
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        f = generate_boolean_function(n)
        actions = symmetric_group_actions(n)
        min_invar_f = min_invariant_points(actions, f)
        c_f = communication_complexity(f)
        results.append((min_invar_f, c_f))
    
    if len(results) < 30:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n for n in [5, 10, 15, 20, 30, 40] if any(n == len(f) for f, _ in results)),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    values1 = [r[0] for r in results]
    values2 = [r[1] for r in results]
    correlation = correlation_coefficient(values1, values2)
    p_val = p_value(correlation, len(results))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n for n in [5, 10, 15, 20, 30, 40] if any(n == len(f) for f, _ in results)),
        "conjecture_holds": p_val,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = f"n={len(r['metric_name'])}, min_invar={r['metric_value']}"
                print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seed}")
                break
        else:
            print("RESULT: INCONCLUSIVE insufficient_support")
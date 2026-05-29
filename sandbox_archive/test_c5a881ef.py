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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def tree_like_resolution_width(f):
        n = len(f)
        if n == 1:
            return 1
        minterms = set()
        for i in range(2**n):
            if f[i] == 0:
                continue
            minterm = []
            for j in range(n):
                if (i >> j) & 1:
                    minterm.append(j)
            minterms.add(tuple(sorted(minterm)))
        width = 0
        while minterms:
            new_minterms = set()
            for m in minterms:
                if len(m) == 1:
                    continue
                v = m[0]
                new_minterms.update({tuple(sorted([x for x in m if x != v]))})
            width += 1
            minterms = new_minterms
        return width
    
    def symplectic_leaves(f):
        n = len(f)
        leaves = set()
        for i in range(2**n):
            if f[i] == 0:
                continue
            leaf = []
            for j in range(n):
                if (i >> j) & 1:
                    leaf.append(j)
            leaves.add(tuple(sorted(leaf)))
        return len(leaves)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        f = generate_boolean_function(n)
        w_t_f = tree_like_resolution_width(f)
        L_f = symplectic_leaves(f)
        results.append({
            "n": n,
            "w_t_f": w_t_f,
            "L_f": L_f
        })
    
    if not results:
        return {
            "metric_name": "symplectic_leaves_number_bounds_tree_like_resolution_width",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_results"
        }
    
    n_max = max(r["n"] for r in results)
    instances_tested = len(results)
    metric_values = [r["L_f"] for r in results]
    w_t_f_squared = [r["w_t_f"]**2 for r in results]
    
    mean_metric_value = sum(metric_values) / instances_tested
    std_metric_value = math.sqrt(sum((x - mean_metric_value)**2 for x in metric_values) / instances_tested)
    
    correlation_coefficient = sum((metric_values[i] - mean_metric_value) * (w_t_f_squared[i] - mean(w_t_f_squared)) for i in range(instances_tested)) / (instances_tested * std_metric_value * math.sqrt(sum((x - mean(w_t_f_squared))**2 for x in w_t_f_squared)))
    
    conjecture_holds = correlation_coefficient > 0.7 and correlation_coefficient < float('inf')
    counterexample = "" if conjecture_holds else "correlation_coefficient={}".format(correlation_coefficient)
    
    return {
        "metric_name": "symplectic_leaves_number_bounds_tree_like_resolution_width",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print("TRIAL:", {"seed": seed, **result})
        results.append(result)
    
    if not results:
        print("RESULT: INCONCLUSIVE no_results")
        sys.exit(1)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print("RESULT: SUPPORTED mean={:.4f} std={:.4f} support_fraction={:.2f}".format(mean_metric_value, std_metric_value, support_fraction))
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print("RESULT: FALSIFIED counterexample=\"{}\" first_failing_seed={}".format(results[0]["counterexample"], first_failing_seed))
    else:
        print("RESULT: INCONCLUSIVE insufficient_support_fraction")
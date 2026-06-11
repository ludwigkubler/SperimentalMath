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
    
    def generate_boolean_instance(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def dpll(instance):
        if not instance:
            return True
        var = instance[0]
        pos_clauses = [c for c in instance if var in c or -var in c]
        neg_clauses = [c for c in instance if -var in c or var in c]
        if any(all(not cl for cl in clause) for clause in pos_clauses):
            return False
        if any(all(cl for cl in clause) for clause in neg_clauses):
            return True
        return dpll([cl for cl in instance[1:] if var not in cl and -var not in cl]) or \
               dpll([cl for cl in instance[1:] if var in cl]) or \
               dpll([cl for cl in instance[1:] if -var in cl])
    
    def hodge_p_structure_order(n):
        # Placeholder function to compute the order of the minimal Hodge p-structure
        return 2**n
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instance = generate_boolean_instance(n)
        height = dpll(instance)
        p_n = hodge_p_structure_order(n)
        results.append({
            "n": n,
            "height": height,
            "p_n": p_n
        })
    
    if not results:
        return {
            "metric_name": "DPLL Height vs Hodge p-Structure Order",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    heights = [r["height"] for r in results]
    p_ns = [r["p_n"] for r in results]
    correlation_coefficient = sum((h - mean(heights)) * (p - mean(p_ns)) for h, p in zip(heights, p_ns)) / \
                                math.sqrt(sum((h - mean(heights))**2 for h in heights) *
                                          sum((p - mean(p_ns))**2 for p in p_ns))
    
    return {
        "metric_name": "DPLL Height vs Hodge p-Structure Order",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": abs(correlation_coefficient) >= 0.8,
        "counterexample": "" if abs(correlation_coefficient) >= 0.8 else "correlation_too_low"
    }

def mean(values):
    return sum(values) / len(values)

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not all(r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_too_low\" first_failing_seed={first_failing_seed}")
    else:
        mean_value = mean([r["metric_value"] for r in results])
        std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
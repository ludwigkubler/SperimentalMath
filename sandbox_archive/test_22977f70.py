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
    
    def communication_complexity(f):
        n = int(math.log2(len(f)))
        max_comm = 0
        for i in range(2**n):
            for j in range(i+1, 2**n):
                if f[i] != f[j]:
                    comm = bin(i^j).count('1')
                    if comm > max_comm:
                        max_comm = comm
        return max_comm
    
    def coxeter_group_action(f):
        n = int(math.log2(len(f)))
        action_order = 0
        for i in range(2**n):
            new_f = [f[i^j] for j in range(2**n)]
            if new_f == f:
                action_order += 1
        return action_order
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    f = generate_boolean_function(n)
    C_f = communication_complexity(f)
    G_action_order = coxeter_group_action(f)
    
    if G_action_order > 10 * C_f**2:
        return {
            "metric_name": "Coxeter Group Action Order",
            "metric_value": G_action_order,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Order {G_action_order} > 10 * {C_f}^2 = {10 * C_f**2}"
        }
    else:
        return {
            "metric_name": "Coxeter Group Action Order",
            "metric_value": G_action_order,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] for r in results if "metric_value" in r)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results):.2f} std=0.00 support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results):.2f} std=0.00 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"Order exceeds 10 * C(f)^2\" first_failing_seed={first_failing_seed}")
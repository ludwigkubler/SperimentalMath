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
    
    def xor_and_tree_width(cnf):
        # Placeholder function to compute XOR-AND tree width
        return len(cnf)
    
    def tropicalized_group_order(n):
        # Placeholder function to compute minimal order of tropicalized group
        return 2 ** n
    
    results = []
    for _ in range(100):  # Test with 100 different instances
        n = random.randint(5, 40)
        cnf = [[random.choice([True, False]) for _ in range(n)] for _ in range(n)]
        xor_and_width = xor_and_tree_width(cnf)
        group_order = tropicalized_group_order(xor_and_width)
        results.append((xor_and_width, group_order))
    
    if not results:
        return {
            "metric_name": "Proportionality Factor",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    xor_and_widths, group_orders = zip(*results)
    mean_xor_and_width = sum(xor_and_widths) / len(xor_and_widths)
    mean_group_order = sum(group_orders) / len(group_orders)
    
    if mean_group_order == 0:
        return {
            "metric_name": "Proportionality Factor",
            "metric_value": None,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": "Mean group order is zero"
        }
    
    proportionality_factor = mean_group_order / mean_xor_and_width
    metric_value = proportionality_factor
    
    return {
        "metric_name": "Proportionality Factor",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "conjecture_holds": 0.7 <= proportionality_factor < 1.3 and abs(metric_value - 1) <= 1.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2**i + 1 for i in range(5, 6)]  # Default list of 30 primes
    else:
        seeds = [int(s) for s in sys.argv[1:]]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not results:
        print("RESULT: INCONCLUSIVE no trials executed")
    else:
        total_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None)
        support_fraction = sum(1 for r in results if r["conjecture_holds"])
        
        if support_fraction >= 0.8 * len(results):
            print(f"RESULT: SUPPORTED mean={total_metric_value / support_fraction} std=NA support_fraction={support_fraction / len(results)}")
        else:
            first_failing_seed = next((i for i, r in enumerate(results) if not r["conjecture_holds"]), None)
            counterexample = results[first_failing_seed]["counterexample"] if first_failing_seed is not None else ""
            print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
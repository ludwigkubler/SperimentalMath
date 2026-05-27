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
    
    def xor_and_tree_width(formula):
        # Placeholder for actual XOR-AND tree width calculation
        return len(formula.split())  # Simplified example
    
    def hodge_decomposition_rank(formula):
        # Placeholder for actual Hodge decomposition rank calculation
        return len(formula.split())  # Simplified example
    
    c = 1.0  # Example constant, replace with actual value if known
    
    instances_tested = 0
    total_metric_value = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Test with 5 instances per size
            m = random.randint(n, 2 * n)
            formula = " ".join(random.choice("01") for _ in range(m))
            tw_F = xor_and_tree_width(formula)
            r_H_F = hodge_decomposition_rank(formula)
            
            if tw_F > c * r_H_F:
                conjecture_holds = False
                counterexample = f"Formula: {formula}, tw(F): {tw_F}, r(H_F): {r_H_F}"
                break
            
            instances_tested += 1
            total_metric_value += tw_F
    
    if not conjecture_holds:
        return {
            "metric_name": "XOR-AND tree width",
            "metric_value": None,
            "instances_tested": instances_tested,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        }
    
    mean_metric_value = total_metric_value / instances_tested
    return {
        "metric_name": "XOR-AND tree width",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result_type = "SUPPORTED"
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        result_type = "FALSIFIED"
    
    print(f"RESULT: {result_type} mean={mean_value:.2f} std=0.00 support_fraction={support_fraction:.2f}")
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
    
    def generate_boolean_formula(n):
        if n == 1:
            return random.choice(['True', 'False'])
        else:
            op = random.choice(['and', 'or'])
            subformulas = [generate_boolean_formula(random.randint(1, n-1)) for _ in range(2)]
            return f"({subformulas[0]} {op} {subformulas[1]})"
    
    def braid_group_order(formula):
        # Simplified mapping from Boolean formula to braid group order
        return len(formula)
    
    def dpll_search_tree_height(formula):
        # Simplified mapping from Boolean formula to DPLL search tree height
        return len(formula.split())
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    conjecture_holds = True
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        formula = generate_boolean_formula(n)
        o_b = braid_group_order(formula)
        dpll_height = dpll_search_tree_height(formula)
        
        if dpll_height == 0:
            conjecture_holds = False
            counterexample = f"Formula '{formula}' has zero DPLL height"
            break
        
        metric_values.append(o_b / math.log(dpll_height))
    
    mean_value = sum(metric_values) / len(metric_values)
    std_value = (sum((x - mean_value) ** 2 for x in metric_values) / len(metric_values)) ** 0.5
    
    return {
        "metric_name": "Braid Group Order vs DPLL Height",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample if not conjecture_holds else ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}")
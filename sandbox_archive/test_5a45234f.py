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
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def truth_table(formula):
        if formula == '0' or formula == '1':
            return [int(formula)]
        elif formula.startswith('not'):
            subformula = formula[4:-1]
            return [1 - val for val in truth_table(subformula)]
        elif formula.startswith('and'):
            left, right = formula[4:-1].split()
            return [val1 and val2 for val1 in truth_table(left) for val2 in truth_table(right)]
        elif formula.startswith('or'):
            left, right = formula[3:-1].split()
            return [val1 or val2 for val1 in truth_table(left) for val2 in truth_table(right)]
    
    def min_p_adic_order(truth_values):
        order = 0
        for value in truth_values:
            if value == 1:
                order += 1
        return order
    
    n = random.randint(5, 40)
    D = random.randint(2, int(n.bit_length()))
    
    # Generate a random Boolean formula of depth D and n variables
    def generate_formula(depth):
        if depth == 0:
            return str(random.choice([0, 1]))
        else:
            op = random.choice(['and', 'or'])
            left = generate_formula(depth - 1)
            right = generate_formula(depth - 1)
            return f"({op} {left} {right})"
    
    formula = generate_formula(D)
    
    truth_values = truth_table(formula)
    min_order = min_p_adic_order(truth_values)
    
    conjecture_holds = min_order <= D
    counterexample = "" if conjecture_holds else f"Formula: {formula}, Min Order: {min_order}, Expected: {D}"
    
    return {
        "metric_name": "Minimal p-adic Order",
        "metric_value": min_order,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_order = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_order} std=NA support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"First failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")
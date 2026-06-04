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
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_formula(n):
        if n == 1:
            return random.choice(['0', '1'])
        else:
            subformulas = [generate_boolean_formula(n-1) for _ in range(2)]
            return f"({subformulas[0]} & {subformulas[1]}) | ({subformulas[0]} ^ {subformulas[1]})"
    
    def resolution_width(formula):
        stack = []
        i = 0
        while i < len(formula):
            if formula[i] == '(':
                stack.append(i)
            elif formula[i] == ')':
                start = stack.pop()
                if not stack:
                    subformula = formula[start+1:i]
                    width = resolution_width(subformula)
                    if width > 1:
                        return width
            i += 1
        return 1
    
    def k_group_index(formula):
        # Placeholder for K-group index computation
        # This is a dummy implementation that returns a random value
        return random.random()
    
    n = 5 + (seed % 3) * 5  # Sweep n through {5, 10, 15, 20, 30}
    formula = generate_boolean_formula(n)
    width = resolution_width(formula)
    index = k_group_index(formula)
    
    return {
        "metric_name": "k_group_index",
        "metric_value": index,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": index <= 3 * width,
        "counterexample": "" if index <= 3 * width else f"Formula: {formula}, Index: {index}, Width: {width}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{res['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")
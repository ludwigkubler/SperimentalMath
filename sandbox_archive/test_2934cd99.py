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
    
    def generate_formula(n):
        if n == 1:
            return 'x'
        else:
            left = generate_formula(n // 2)
            right = generate_formula(n - n // 2)
            return f'({left} & {right}) | ({left} ^ {right})'
    
    def count_literals(formula):
        if formula[0] in ('&', '|'):
            return count_literals(formula[1]) + count_literals(formula[3])
        else:
            return 1
    
    def prove_length(formula):
        if formula[0] == '&':
            return 1 + max(prove_length(formula[1]), prove_length(formula[3]))
        elif formula[0] == '|':
            return 1 + min(prove_length(formula[1]), prove_length(formula[3]))
        else:
            return 1
    
    def tropical_norm(formula):
        if formula[0] in ('&', '|'):
            return max(tropical_norm(formula[1]), tropical_norm(formula[3]))
        else:
            return 1
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    formula = generate_formula(n)
    literals = count_literals(formula)
    proof_length = prove_length(formula)
    norm = tropical_norm(formula)
    
    c = 1.0
    bound = n ** c * proof_length
    
    if norm > 1.1 * bound:
        return {
            "metric_name": "tropical_norm",
            "metric_value": norm,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": f"Formula: {formula}, Norm: {norm}, Bound: {bound}"
        }
    
    return {
        "metric_name": "tropical_norm",
        "metric_value": norm,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if r["conjecture_holds"]]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values):.2f} std={math.sqrt(sum((x - sum(metric_values)/len(metric_values))**2 for x in metric_values) / len(metric_values)):.2f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Formula too complex\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")
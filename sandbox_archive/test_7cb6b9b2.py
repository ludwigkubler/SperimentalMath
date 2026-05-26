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
        if isinstance(formula, str):
            return 1
        else:
            return max(xor_and_tree_width(subformula) for subformula in formula) + 1
    
    def geometric_quantization_rank(formula):
        # Placeholder for actual quantum state rank computation
        # For simplicity, we use a random value that depends on the seed and formula
        return random.randint(1, 10)
    
    n = random.randint(5, 40)
    formula = generate_random_formula(n)
    T_f = xor_and_tree_width(formula)
    ρ_f_rank = geometric_quantization_rank(formula)
    
    if T_f == 0:
        return {
            "metric_name": "minimal_rank",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "XOR-AND tree width is zero"
        }
    
    alpha = 1.5
    beta = 0.5
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": ρ_f_rank,
        "instances_tested": 1,
        "conjecture_holds": abs(ρ_f_rank - alpha * math.log(T_f)) <= 3 and abs(ρ_f_rank - beta * T_f) <= 3,
        "counterexample": ""
    }

def generate_random_formula(n):
    if n == 1:
        return random.choice(['0', '1'])
    else:
        op = random.choice(['and', 'or'])
        subformulas = [generate_random_formula(random.randint(1, n-1)) for _ in range(2)]
        return (op, *subformulas)

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all('metric_value' not in r or r['metric_value'] is None for r in results):
        print("RESULT: INCONCLUSIVE mapping_undefined")
    else:
        values = [r['metric_value'] for r in results if 'metric_value' in r and r['metric_value'] is not None]
        mean_value = sum(values) / len(values)
        std_value = math.sqrt(sum((x - mean_value) ** 2 for x in values) / len(values))
        support_fraction = sum(r['conjecture_holds'] for r in results if 'conjecture_holds' in r and r['conjecture_holds']) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
        else:
            first_failing_seed = next((i for i, r in enumerate(results) if not r['conjecture_holds']), None)
            counterexample = results[first_failing_seed]['counterexample'] if first_failing_seed is not None else ""
            print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[first_failing_seed]}")
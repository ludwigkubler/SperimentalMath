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
    
    def xor_and_tree_width(formula):
        if isinstance(formula, str):
            return 1
        elif formula[0] == 'XOR':
            return 1 + max(xor_and_tree_width(subformula) for subformula in formula[1:])
        elif formula[0] == 'AND':
            return 1 + sum(xor_and_tree_width(subformula) for subformula in formula[1:])
    
    def generate_random_boolean_function(n):
        if n == 1:
            return random.choice(['0', '1'])
        else:
            op = random.choice(['XOR', 'AND'])
            return [op] + [generate_random_boolean_function(random.randint(1, n)) for _ in range(random.randint(2, n))]
    
    def geometric_quantization(formula):
        if isinstance(formula, str):
            return {formula: 1}
        elif formula[0] == 'XOR':
            left = geometric_quantization(formula[1])
            right = geometric_quantization(formula[2])
            result = {}
            for k in set(left.keys()).union(right.keys()):
                result[k] = (left.get(k, 0) + right.get(k, 0)) % 2
            return result
        elif formula[0] == 'AND':
            left = geometric_quantization(formula[1])
            right = geometric_quantization(formula[2])
            result = {}
            for k in set(left.keys()).intersection(right.keys()):
                result[k] = (left.get(k, 0) * right.get(k, 0)) % 2
            return result
    
    def rank_of_quantum_state(state):
        return len([k for k, v in state.items() if v == 1])
    
    n = random.randint(5, 40)
    formula = generate_random_boolean_function(n)
    T_f = xor_and_tree_width(formula)
    ρ_f = geometric_quantization(formula)
    rk_ρ_f = rank_of_quantum_state(ρ_f)
    
    α = Fraction(1, 2)  # Example constant
    β = Fraction(1, 4)  # Example constant
    
    if T_f == 0:
        return {
            "metric_name": "rank_of_quantum_state",
            "metric_value": rk_ρ_f,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "XOR-AND tree width is zero"
        }
    
    lower_bound = α * math.log(T_f)
    upper_bound = β * T_f
    
    return {
        "metric_name": "rank_of_quantum_state",
        "metric_value": rk_ρ_f,
        "instances_tested": 1,
        "conjecture_holds": abs(rk_ρ_f - lower_bound) <= 3 and abs(rk_ρ_f - upper_bound) <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_dev = math.sqrt(sum((x - mean_value)**2 for x in (result["metric_value"] for result in results)) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = next(result["counterexample"] for result in results if result["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
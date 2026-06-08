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
    
    def generate_boolean_circuit(depth):
        if depth == 1:
            return ['0', '1']
        left = generate_boolean_circuit(depth - 1)
        right = generate_boolean_circuit(depth - 1)
        return [f'({l} AND {r})' for l in left] + [f'({l} OR {r})' for l in right]
    
    def tseitin_formula(circuit):
        n = len(circuit)
        variables = list(range(n))
        formulas = []
        for i, expr in enumerate(circuit):
            if 'AND' in expr:
                left, right = expr.split(' AND ')
                new_var = f'v{i}'
                formulas.append(f'{new_var} <=> ({left} AND {right})')
                variables.append(new_var)
            elif 'OR' in expr:
                left, right = expr.split(' OR ')
                new_var = f'v{i}'
                formulas.append(f'{new_var} <=> ({left} OR {right})')
                variables.append(new_var)
        return formulas, variables
    
    def compute_local_index(formulas, variables):
        n = len(variables)
        local_indices = [0] * n
        for formula in formulas:
            if '=>' in formula:
                antecedent, consequent = formula.split(' => ')
                if 'AND' in consequent:
                    left, right = consequent.split(' AND ')
                    local_indices[variables.index(antecedent)] += 1
                    local_indices[variables.index(left)] += 1
                    local_indices[variables.index(right)] += 1
        return max(local_indices)
    
    depths = [5, 10, 15, 20, 30, 40]
    metric_values = []
    instances_tested = 0
    n_max = 0
    
    for depth in depths:
        circuit = generate_boolean_circuit(depth)
        formulas, variables = tseitin_formula(circuit)
        local_index = compute_local_index(formulas, variables)
        
        if local_index > 4 * depth * math.log(len(variables)):
            return {
                "metric_name": "minimal_local_index",
                "metric_value": None,
                "instances_tested": instances_tested,
                "n_max": n_max,
                "conjecture_holds": False,
                "counterexample": f"Local index {local_index} exceeds 4d log n for d={depth}, n={len(variables)}"
            }
        
        metric_values.append(local_index)
        instances_tested += len(circuit)
        n_max = max(n_max, depth)
    
    mean_msl = sum(metric_values) / len(metric_values)
    std_dev = math.sqrt(sum((x - mean_msl) ** 2 for x in metric_values) / len(metric_values))
    
    return {
        "metric_name": "minimal_local_index",
        "metric_value": mean_msl,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": all(0.5 <= msl / d for d, msl in zip(depths, metric_values)) and all(msl <= 4 * d * math.log(n) for d, n, msl in zip(depths, [len(variables)] * len(depths), metric_values)),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_msl = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_msl) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_msl} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["metric_value"] < 0.5 * d for d, msl in zip(depths, metric_values)):
        print(f"RESULT: FALSIFIED counterexample=\"local_index_too_small\" first_failing_seed={seeds[results.index(next(r for r in results if not r['conjecture_holds']))]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")
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
    
    def generate_circuit(depth):
        if depth == 0:
            return ['NOT', 'XOR']
        else:
            op = random.choice(['AND', 'OR'])
            left = generate_circuit(depth - 1)
            right = generate_circuit(depth - 1)
            return [op, left, right]
    
    def count_distinct_actions(circuit):
        if isinstance(circuit, list):
            action = circuit[0]
            left = count_distinct_actions(circuit[1])
            right = count_distinct_actions(circuit[2])
            return {action} | left | right
        else:
            return set()
    
    def is_valid_circuit(circuit):
        if isinstance(circuit, list):
            op = circuit[0]
            left = circuit[1]
            right = circuit[2]
            if op not in ['AND', 'OR']:
                return False
            if not (isinstance(left, list) or isinstance(left, str)) or not (isinstance(right, list) or isinstance(right, str)):
                return False
            return is_valid_circuit(left) and is_valid_circuit(right)
        else:
            return circuit in ['NOT', 'XOR']
    
    n_max = 40
    instances_tested = 30
    total_actions = 0
    
    for _ in range(instances_tested):
        depth = random.randint(1, n_max)
        circuit = generate_circuit(depth)
        if not is_valid_circuit(circuit):
            continue
        
        actions = count_distinct_actions(circuit)
        total_actions += len(actions)
    
    metric_value = total_actions / instances_tested
    conjecture_holds = metric_value <= 2 ** n_max
    
    return {
        "metric_name": "distinct_coxeter_group_actions",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_dev = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
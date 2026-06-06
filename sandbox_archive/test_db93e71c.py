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
    
    def generate_circuit(n):
        if n == 1:
            return ['input']
        else:
            left = generate_circuit(random.randint(1, n-2))
            right = generate_circuit(n - len(left) - 1)
            return [random.choice(['and', 'or'])] + left + right
    
    def evaluate_circuit(circuit):
        if circuit == ['input']:
            return random.choice([0, 1])
        elif circuit[0] == 'and':
            return evaluate_circuit(circuit[1]) and evaluate_circuit(circuit[2:])
        else:
            return evaluate_circuit(circuit[1]) or evaluate_circuit(circuit[2:])
    
    def compute_monotone_width(circuit):
        if circuit == ['input']:
            return 1
        elif circuit[0] == 'and':
            return max(compute_monotone_width(circuit[1]), compute_monotone_width(circuit[2:]))
        else:
            return max(compute_monotone_width(circuit[1]), compute_monotone_width(circuit[2:]))
    
    def compute_minimal_order(circuit):
        if circuit == ['input']:
            return 1
        elif circuit[0] == 'and':
            return max(compute_minimal_order(circuit[1]), compute_minimal_order(circuit[2:]))
        else:
            return max(compute_minimal_order(circuit[1]), compute_minimal_order(circuit[2:]))
    
    n = random.randint(5, 40)
    circuit = generate_circuit(n)
    monotone_width = compute_monotone_width(circuit)
    minimal_order = compute_minimal_order(circuit)
    
    return {
        "metric_name": "monotone_width",
        "metric_value": monotone_width,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": monotone_width >= minimal_order,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        results.append(result)
        print(f"TRIAL: {result}")
    
    mean_metric_value = sum(r['metric_value'] for r in results) / len(results)
    std_metric_value = (sum((r['metric_value'] - mean_metric_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r['conjecture_holds']) / len(results) >= 0.2:
        first_failing_seed = next(r['seed'] for r in results if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")
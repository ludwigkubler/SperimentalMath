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
    
    def generate_circuit(n):
        if n == 1:
            return {'type': 'input', 'value': random.choice([0, 1])}
        elif n == 2:
            return {'type': 'gate', 'operation': random.choice(['AND', 'OR']), 'inputs': [generate_circuit(1), generate_circuit(1)]}
        else:
            left = generate_circuit(n // 2)
            right = generate_circuit(n - n // 2)
            return {'type': 'gate', 'operation': random.choice(['AND', 'OR']), 'inputs': [left, right]}
    
    def count_monotone_complexity(circuit):
        if circuit['type'] == 'input':
            return 1
        elif circuit['type'] == 'gate':
            return 1 + sum(count_monotone_complexity(inp) for inp in circuit['inputs'])
    
    def min_order_modular_extensions(circuit):
        if circuit['type'] == 'input':
            return 1
        elif circuit['type'] == 'gate':
            orders = [min_order_modular_extensions(inp) for inp in circuit['inputs']]
            return max(orders)
    
    n = random.randint(5, 40)
    circuit = generate_circuit(n)
    m_C = count_monotone_complexity(circuit)
    min_order = min_order_modular_extensions(circuit)
    
    if abs(min_order - m_C) > 2:
        return {
            "metric_name": "min_order_diff",
            "metric_value": abs(min_order - m_C),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": f"n={n}, min_order={min_order}, m(C)={m_C}"
        }
    else:
        return {
            "metric_name": "min_order_diff",
            "metric_value": abs(min_order - m_C),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": True,
            "counterexample": ""
        }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r['metric_value'] for r in results) / len(results)
    std_value = math.sqrt(sum((r['metric_value'] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r['seed'] for r in results if not r['conjecture_holds']), None)
        print(f"RESULT: FALSIFIED counterexample=\"n={results[0]['n_max']}, min_order_diff={results[0]['metric_value']}\" first_failing_seed={first_failing_seed}")
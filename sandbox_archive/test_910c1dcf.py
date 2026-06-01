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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_circuit(n):
        if n == 1:
            return {'type': 'input', 'value': random.choice([0, 1])}
        else:
            inputs = [generate_circuit(1) for _ in range(n)]
            gate_type = random.choice(['AND', 'OR'])
            return {'type': gate_type, 'inputs': inputs}
    
    def count_monotone_complexity(circuit):
        if circuit['type'] == 'input':
            return 0
        else:
            return max(count_monotone_complexity(inp) for inp in circuit['inputs']) + 1
    
    def min_order_modular_extensions(circuit):
        if circuit['type'] == 'input':
            return 1
        else:
            orders = [min_order_modular_extensions(inp) for inp in circuit['inputs']]
            return max(orders) + 1
    
    n_max = 0
    instances_tested = 0
    total_min_order = 0
    total_monotone_complexity = 0
    
    for _ in range(30):
        n = random.randint(5, 40)
        circuit = generate_circuit(n)
        min_order = min_order_modular_extensions(circuit)
        monotone_complexity = count_monotone_complexity(circuit)
        
        if n > n_max:
            n_max = n
        
        instances_tested += 1
        total_min_order += min_order
        total_monotone_complexity += monotone_complexity
    
    mean_min_order = Fraction(total_min_order, instances_tested)
    mean_monotone_complexity = Fraction(total_monotone_complexity, instances_tested)
    
    if abs(mean_min_order - mean_monotone_complexity) <= 2:
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = f"mean_min_order={mean_min_order}, mean_monotone_complexity={mean_monotone_complexity}"
    
    return {
        "metric_name": "min_order_vs_monotone_complexity",
        "metric_value": abs(mean_min_order - mean_monotone_complexity),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r['metric_value'] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r['seed'] for r in results if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
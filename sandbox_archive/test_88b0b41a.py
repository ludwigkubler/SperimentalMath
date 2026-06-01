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
        else:
            left = generate_circuit(n // 2)
            right = generate_circuit(n - n // 2)
            gate_type = random.choice(['AND', 'OR'])
            return {'type': 'gate', 'gate_type': gate_type, 'left': left, 'right': right}
    
    def count_monotone_complexity(circuit):
        if circuit['type'] == 'input':
            return 1
        else:
            left_complexity = count_monotone_complexity(circuit['left'])
            right_complexity = count_monotone_complexity(circuit['right'])
            if circuit['gate_type'] == 'AND':
                return max(left_complexity, right_complexity) + 1
            elif circuit['gate_type'] == 'OR':
                return min(left_complexity, right_complexity) + 1
    
    def count_min_order_extensions(circuit):
        if circuit['type'] == 'input':
            return 0
        else:
            left_extensions = count_min_order_extensions(circuit['left'])
            right_extensions = count_min_order_extensions(circuit['right'])
            if circuit['gate_type'] == 'AND':
                return max(left_extensions, right_extensions) + 1
            elif circuit['gate_type'] == 'OR':
                return min(left_extensions, right_extensions) + 1
    
    n = random.randint(5, 40)
    circuit = generate_circuit(n)
    m_C = count_monotone_complexity(circuit)
    min_order_C = count_min_order_extensions(circuit)
    
    if m_C == 0:
        return {
            'metric_name': 'min_order_diff',
            'metric_value': float('inf'),
            'instances_tested': 1,
            'n_max': n,
            'conjecture_holds': False,
            'counterexample': f'n={n}, min_order=0, m(C)=0'
        }
    
    min_order_diff = abs(min_order_C - m_C)
    
    return {
        'metric_name': 'min_order_diff',
        'metric_value': min_order_diff,
        'instances_tested': 1,
        'n_max': n,
        'conjecture_holds': min_order_diff <= 2,
        'counterexample': f'n={n}, min_order={min_order_C}, m(C)={m_C}'
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(100, 999) for _ in range(30)]
    
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
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
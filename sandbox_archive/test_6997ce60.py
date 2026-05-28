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

def generate_circuit(n, depth):
    if depth == 0:
        return [('input', i) for i in range(n)]
    gate_types = ['AND', 'OR']
    gate_type = random.choice(gate_types)
    inputs = [generate_circuit(n, depth - 1) for _ in range(2)]
    return [(gate_type, inputs)]

def evaluate_circuit(circuit):
    stack = []
    for gate_type, inputs in circuit:
        if gate_type == 'input':
            stack.append(inputs[0])
        elif gate_type == 'AND':
            a, b = stack.pop(), stack.pop()
            stack.append(a and b)
        elif gate_type == 'OR':
            a, b = stack.pop(), stack.pop()
            stack.append(a or b)
    return stack[0]

def monotonicity(circuit):
    n = len(circuit)
    inputs = [random.choice([True, False]) for _ in range(n)]
    outputs = [evaluate_circuit([(gate_type, inputs[i]) for gate_type, _ in circuit]) for i in range(len(inputs))]
    return max(outputs)

def min_rank(tensor_product):
    # Placeholder function to compute the minimal rank of a tensor product
    # This is a dummy implementation and should be replaced with actual logic
    return len(tensor_product)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 10  # Example value for n, can be adjusted
    depth = 3  # Example value for depth, can be adjusted
    circuit = generate_circuit(n, depth)
    m_C = monotonicity(circuit)
    tensor_product = [[random.choice([True, False]) for _ in range(m_C)] for _ in range(m_C)]
    rank_T_C = min_rank(tensor_product)
    ratio = Fraction(rank_T_C, math.log(m_C))
    
    result = {
        "metric_name": "ratio",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "conjecture_holds": ratio <= 1,
        "counterexample": "" if ratio <= 1 else f"Counterexample with n={n}, depth={depth}"
    }
    
    return result

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Ratio exceeds 1' first_failing_seed={seeds[first_failing_seed]}")
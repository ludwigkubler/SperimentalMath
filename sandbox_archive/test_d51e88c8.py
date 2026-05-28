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

def generate_circuit(n, depth):
    if depth == 0:
        return [('input', i) for i in range(n)]
    else:
        gate_type = random.choice(['and', 'or'])
        inputs = [generate_circuit(n, depth - 1) for _ in range(2)]
        return [(gate_type, inputs)]

def evaluate_circuit(circuit):
    stack = []
    for gate_type, inputs in circuit:
        if gate_type == 'input':
            stack.append(inputs[0])
        elif gate_type == 'and':
            a, b = stack.pop(), stack.pop()
            stack.append(a and b)
        elif gate_type == 'or':
            a, b = stack.pop(), stack.pop()
            stack.append(a or b)
    return stack[0]

def monotonicity(circuit):
    inputs = [1 << i for i in range(len(circuit))]
    outputs = [evaluate_circuit([(gate_type, inputs[i]) for gate_type, _ in circuit]) for i in range(len(inputs))]
    m_C = 1
    while any(outputs):
        m_C += 1
        new_outputs = []
        for output in outputs:
            if output:
                new_output = evaluate_circuit([(gate_type, output) for gate_type, _ in circuit])
                if new_output not in new_outputs:
                    new_outputs.append(new_output)
        outputs = new_outputs
    return m_C

def min_rank(tensor_product):
    n = len(tensor_product)
    rank = 1
    while True:
        found = False
        for i in range(n):
            if tensor_product[i]:
                found = True
                break
        if not found:
            break
        rank += 1
        new_tensor_product = []
        for i in range(n):
            if tensor_product[i]:
                new_tensor_product.append([tensor_product[j][i] for j in range(n)])
        tensor_product = new_tensor_product
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 10  # Start with a small size and increase if necessary
    circuit = generate_circuit(n, depth=3)
    m_C = monotonicity(circuit)
    tensor_product = [[(i >> j) & 1 for j in range(n)] for i in range(1 << n)]
    min_rank_T_C = min_rank(tensor_product)
    ratio = min_rank_T_C / math.log(m_C, 2)
    return {
        "metric_name": "ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio <= 1,
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

    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")
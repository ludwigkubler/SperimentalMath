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
        return [(random.choice(['AND', 'OR']), [f'x{i}' for i in range(n)])]
    else:
        gate_type = random.choice(['NOT', 'AND', 'OR'])
        inputs = [generate_circuit(n, depth - 1) for _ in range(2)]
        if gate_type == 'NOT':
            return [(gate_type, inputs[0])]
        else:
            return [(gate_type, inputs[0], inputs[1])]

def evaluate_circuit(circuit):
    stack = []
    for gate_type, *inputs in circuit:
        if gate_type == 'NOT':
            a = stack.pop()
            stack.append(not a)
        elif gate_type == 'AND':
            a, b = stack.pop(), stack.pop()
            stack.append(a and b)
        elif gate_type == 'OR':
            a, b = stack.pop(), stack.pop()
            stack.append(a or b)
    return stack[0]

def monotonicity(circuit):
    inputs = ['x' + str(i) for i in range(len(circuit[0][1]))]
    outputs = [evaluate_circuit([(gate_type, inputs[i]) for gate_type, _ in circuit]) for i in range(len(inputs))]
    return max(outputs)

def min_rank(tensor_product):
    # Placeholder for actual computation
    return len(tensor_product)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    depth = random.randint(1, 3)
    circuit = generate_circuit(n, depth)
    m_C = monotonicity(circuit)
    tensor_product = [[random.choice([0, 1]) for _ in range(m_C)] for _ in range(m_C)]
    rank = min_rank(tensor_product)
    ratio = rank / math.log(m_C) if m_C > 0 else float('inf')
    return {
        "metric_name": "Ratio of Min Rank to Log Monotonicity",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio <= 1,
        "counterexample": "" if ratio <= 1 else "Monotonicity degree too high for given rank"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=NA support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Monotonicity degree too high for given rank\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")
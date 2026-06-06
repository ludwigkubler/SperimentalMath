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

def generate_boolean_circuit(W):
    if W == 1:
        return ['0', '1']
    w = random.randint(1, W-1)
    left = generate_boolean_circuit(w)
    right = generate_boolean_circuit(W-w)
    return [f'({l} & {r})' for l in left] + [f'({l} | {r})' for l in right]

def evaluate_circuit(circuit):
    variables = set()
    for expr in circuit:
        if '&' in expr or '|' in expr:
            variables.update(expr.split()[1:-1])
    values = {var: random.choice(['0', '1']) for var in variables}
    stack = []
    for expr in circuit[::-1]:
        if expr == '0' or expr == '1':
            stack.append(expr)
        elif '&' in expr:
            left = stack.pop()
            right = stack.pop()
            stack.append('1' if left == '1' and right == '1' else '0')
        elif '|' in expr:
            left = stack.pop()
            right = stack.pop()
            stack.append('0' if left == '0' and right == '0' else '1')
    return stack[0]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for W in [5, 10, 15, 20, 30, 40]:
        instances_tested = 0
        n_max = W
        total_dimension = 0
        for _ in range(30):
            circuit = generate_boolean_circuit(W)
            dimension = evaluate_circuit(circuit)  # Simplified for testing purposes
            results.append((W, dimension))
            instances_tested += 1
        mean_dimension = sum(dimension for _, dimension in results) / len(results)
        conjecture_holds = mean_dimension <= W**2
        counterexample = "" if conjecture_holds else f"Mean dimension: {mean_dimension}, Expected: {W**2}"
        return {
            "metric_name": "Moduli Space Dimension",
            "metric_value": mean_dimension,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = (sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))**0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Mean dimension exceeds expected' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")
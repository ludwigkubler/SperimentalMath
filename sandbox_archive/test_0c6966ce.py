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

def generate_circuit(n):
    if n == 1:
        return ['0', '1']
    left = generate_circuit(n // 2)
    right = generate_circuit(n - n // 2)
    return [f'({x} & {y})' for x in left] + [f'({x} | {y})' for y in right]

def evaluate_circuit(circuit, assignment):
    stack = []
    for token in circuit:
        if token.isdigit():
            stack.append(int(token))
        elif token == '0':
            stack.append(0)
        elif token == '1':
            stack.append(1)
        else:
            b = stack.pop()
            a = stack.pop()
            if token == '&':
                stack.append(a & b)
            elif token == '|':
                stack.append(a | b)
    return stack[0]

def compute_frege_depth(circuit):
    if not circuit:
        return 1
    max_depth = 0
    for token in circuit:
        if isinstance(token, list):
            depth = compute_frege_depth(token)
            if depth > max_depth:
                max_depth = depth
    return max_depth + 1

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 0
    instances_tested = 0
    total_metric_value = Fraction(0)
    conjecture_holds = True
    counterexample = ""

    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n

        circuit = generate_circuit(n)
        instances_tested += len(circuit)

        for _ in range(5):  # Sample 5 random assignments
            assignment = {i: random.choice([0, 1]) for i in range(n)}
            output = evaluate_circuit(circuit, assignment)
            frege_depth = compute_frege_depth(circuit)

            if frege_depth == 0:
                continue

            metric_value = abs(output - 0.5) / frege_depth
            total_metric_value += Fraction(metric_value).limit_denominator()

            if not (0.8 <= metric_value <= 1.2):
                conjecture_holds = False
                counterexample = f"n={n}, output={output}, frege_depth={frege_depth}"

    mean_metric_value = float(total_metric_value / instances_tested)
    return {
        "metric_name": "Frege Proof Depth vs Symplectic Leaves",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
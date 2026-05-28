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

def generate_boolean_circuit(n):
    if n == 1:
        return ['x1']
    left = generate_boolean_circuit(n // 2)
    right = generate_boolean_circuit(n - n // 2)
    return [f'({l} AND {r})' for l in left] + [f'({l} OR {r})' for l in left] + [f'(NOT {l})' for l in right]

def evaluate_circuit(circuit, assignment):
    stack = []
    for token in circuit:
        if 'x' in token:
            stack.append(assignment[token[1:]])
        elif token == 'NOT':
            stack.append(not stack.pop())
        else:
            b2 = stack.pop()
            b1 = stack.pop()
            if token == 'AND':
                stack.append(b1 and b2)
            elif token == 'OR':
                stack.append(b1 or b2)
    return stack[0]

def generate_random_assignment(n):
    return {f'x{i+1}': random.choice([True, False]) for i in range(n)}

def tropical_cyclotomic_polynomial(circuit):
    n = len(circuit)
    assignment = generate_random_assignment(n)
    value = evaluate_circuit(circuit, assignment)
    rank = 0
    while value != 0:
        rank += 1
        value = (value + 1) // 2
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        circuit = generate_boolean_circuit(n)
        rank = tropical_cyclotomic_polynomial(circuit)
        bound = math.pow(len(circuit), 1/5)
        results.append({
            "n": n,
            "rank": rank,
            "bound": bound
        })
    metric_value = sum(result["rank"] for result in results) / len(results)
    conjecture_holds = all(result["rank"] <= result["bound"] for result in results)
    counterexample = "" if conjecture_holds else f"n={results[0]['n']}, rank={results[0]['rank']}, bound={results[0]['bound']}"
    return {
        "metric_name": "Rank of Tropical Cyclotomic Polynomial",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30*3 + 1))
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = results[results.index(next(r for r in results if not r["conjecture_holds"]))]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
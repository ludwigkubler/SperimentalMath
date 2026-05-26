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

def generate_circuit(w, d):
    if w == 1 and d == 0:
        return random.choice(['x1', 'x2', 'x3'])
    else:
        left = generate_circuit(w//2, d-1)
        right = generate_circuit(w//2, d-1)
        op = random.choice(['&', '|'])
        return f"({left} {op} {right})"

def evaluate_circuit(circuit):
    stack = []
    ops = {'&': lambda a, b: a and b, '|': lambda a, b: a or b}
    for token in circuit.replace(' ', ''):
        if token in ops:
            b = stack.pop()
            a = stack.pop()
            stack.append(ops[token](a, b))
        else:
            stack.append(token == 'x1')
    return stack[0]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            w = random.randint(1, n)
            d = random.randint(1, n)
            circuit = generate_circuit(w, d)
            result = evaluate_circuit(circuit)
            results.append((w, d, result))
    min_rank = max(len(result) for _, _, result in results)
    conjecture_holds = min_rank >= 2**(n/2 + 1)
    counterexample = "" if conjecture_holds else f"min_rank={min_rank} < 2^{n/2 + 1}"
    return {
        "metric_name": "minimal_rank",
        "metric_value": min_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 1 for i in range(5, 30)]
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
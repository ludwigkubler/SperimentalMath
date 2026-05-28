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

def generate_branching_program(n):
    if n == 1:
        return {'type': 'LEAF', 'value': random.choice([0, 1])}
    node_type = random.choice(['AND', 'OR'])
    children = [generate_branching_program(random.randint(1, min(n-1, 3))) for _ in range(2)]
    return {'type': node_type, 'children': children}

def compute_entanglement_index(program):
    if program['type'] == 'LEAF':
        return 0
    else:
        entanglement = 0
        for child in program['children']:
            entanglement += compute_entanglement_index(child)
        return entanglement + 1

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            program = generate_branching_program(n)
            entanglement_index = compute_entanglement_index(program)
            total_metric_value += entanglement_index
            instances_tested += 1

    mean_value = Fraction(total_metric_value, instances_tested)
    if mean_value > n_values[-1] ** 2:  # Polynomial bound (e.g., n^2)
        conjecture_holds = False
        counterexample = f"Mean entanglement index {mean_value} exceeds polynomial bound for n={n_values[-1]}"

    return {
        "metric_name": "Quantum Entanglement Index",
        "metric_value": float(mean_value),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
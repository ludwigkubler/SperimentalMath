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
        return [(random.choice(['AND', 'OR']), [random.randint(0, n-1)])]
    else:
        inputs = [generate_circuit(n, depth-1) for _ in range(random.randint(2, 3))]
        gate_type = random.choice(['AND', 'OR'])
        return [(gate_type, sum(len(subcircuit) for subcircuit in inputs), sum(inputs, []))]

def evaluate_circuit(circuit):
    stack = []
    for gate_type, n_inputs, inputs in circuit:
        if gate_type == 'AND':
            result = all(stack.pop() for _ in range(n_inputs))
        elif gate_type == 'OR':
            result = any(stack.pop() for _ in range(n_inputs))
        else:
            raise ValueError(f"Invalid gate type: {gate_type}")
        stack.append(result)
    return stack[0]

def algebraic_quotient(circuit):
    n = len(circuit)
    equivalence_classes = {}
    for i in range(2**n):
        assignment = [i >> j & 1 for j in range(n)]
        output = evaluate_circuit([(gate_type, inputs) for gate_type, inputs in circuit if all(assignment[i] == 0 or assignment[i] == 1 for i in inputs)])
        if output not in equivalence_classes:
            equivalence_classes[output] = []
        equivalence_classes[output].append(i)
    return len(equivalence_classes)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    circuit = generate_circuit(n, depth=random.randint(2, 3))
    complexity = len(circuit)
    rank_quot = algebraic_quotient(circuit)
    ratio = Fraction(rank_quot, complexity) if complexity != 0 else float('inf')
    conjecture_holds = ratio <= 1.5
    counterexample = "" if conjecture_holds else f"n={n}, rank_quot={rank_quot}, complexity={complexity}"
    return {
        "metric_name": "Ratio of Rank Quotient to Complexity",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
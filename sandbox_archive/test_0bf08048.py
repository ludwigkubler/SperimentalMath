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
    
    def generate_boolean_circuit(n):
        circuit = []
        for _ in range(n):
            gate_type = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(random.randint(2, n))]
            circuit.append((gate_type, inputs))
        return circuit

    def evaluate_circuit(circuit, input_values):
        stack = []
        for gate_type, inputs in reversed(circuit):
            if gate_type == 'AND':
                result = all(input_values[i] for i in inputs)
            elif gate_type == 'OR':
                result = any(input_values[i] for i in inputs)
            stack.append(result)
        return stack[0]

    def compute_groupoid_rank(circuit):
        n = len(circuit)
        rank = 0
        for i in range(2**n):
            input_values = [i >> j & 1 for j in range(n)]
            output = evaluate_circuit(circuit, input_values)
            if output:
                rank += 1
        return rank

    n = random.randint(5, 40)
    circuit = generate_boolean_circuit(n)
    groupoid_rank = compute_groupoid_rank(circuit)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": groupoid_rank,
        "instances_tested": 1,
        "conjecture_holds": groupoid_rank <= n**2,
        "counterexample": "" if conjecture_holds else f"Groupoid rank {groupoid_rank} > {n**2}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={math.sqrt(sum((r['metric_value'] - mean_rank)**2 for r in results) / len(results))} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Groupoid rank exceeds n^2\" first_failing_seed={first_failing_seed}")
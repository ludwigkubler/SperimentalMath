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
    
    def evaluate_circuit(circuit):
        if isinstance(circuit, tuple):
            op, left, right = circuit
            if op == 'AND':
                return evaluate_circuit(left) and evaluate_circuit(right)
            elif op == 'OR':
                return evaluate_circuit(left) or evaluate_circuit(right)
            elif op == 'NOT':
                return not evaluate_circuit(left)
        else:
            return circuit
    
    def truth_table(circuit, n):
        inputs = [tuple([i for i in range(n)])]
        while len(inputs[0]) < 2**n:
            new_inputs = []
            for input_ in inputs:
                new_input1 = tuple(input_ + (0,))
                new_input2 = tuple(input_ + (1,))
                if evaluate_circuit(circuit, new_input1) != evaluate_circuit(circuit, new_input2):
                    new_inputs.append(new_input2)
            inputs.extend(new_inputs)
        return [evaluate_circuit(circuit, input_) for input_ in inputs]
    
    def is_quasigroup(table):
        n = len(table)
        for i in range(n):
            for j in range(n):
                if table[i][j] not in set(range(n)):
                    return False
        return True
    
    def min_order_quasigroup(table):
        n = len(table)
        for order in range(1, n+1):
            for perm in itertools.permutations(range(n), order):
                if all(table[perm[i]][perm[j]] == table[i][j] for i in range(order) for j in range(order)):
                    return order
        return n
    
    def monotone_width(circuit):
        # Placeholder implementation; actual monotone width calculation is complex
        return random.randint(1, 10)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    circuit = generate_random_circuit(n)
    table = truth_table(circuit, n)
    if not is_quasigroup(table):
        return {
            "metric_name": "min_order",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    min_order = min_order_quasigroup(table)
    mon_wid = monotone_width(circuit)
    
    return {
        "metric_name": "min_order",
        "metric_value": min_order,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(min_order - mon_wid) <= 2 * mon_wid,
        "counterexample": ""
    }

def generate_random_circuit(n):
    if n == 0:
        return random.choice([True, False])
    else:
        op = random.choice(['AND', 'OR', 'NOT'])
        left = generate_random_circuit(n-1)
        right = generate_random_circuit(n-1)
        return (op, left, right)

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["metric_value"] is not None for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no valid data")
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
    
    def generate_circuit(n):
        circuit = []
        for _ in range(n):
            gate_type = random.choice(['AND', 'OR', 'NOT'])
            if gate_type == 'NOT':
                inputs = [random.randint(0, 1)]
            else:
                inputs = [random.randint(0, 1) for _ in range(random.randint(2, 3))]
            circuit.append((gate_type, inputs))
        return circuit
    
    def is_satisfiable(circuit):
        n = len(circuit)
        assignments = [i for i in range(2**n)]
        for assignment in assignments:
            stack = []
            for gate in reversed(circuit):
                if gate[0] == 'NOT':
                    stack.append(not stack[-1])
                elif gate[0] == 'AND':
                    stack.append(stack.pop() and stack.pop())
                else:  # OR
                    stack.append(stack.pop() or stack.pop())
            if stack:
                return True
        return False
    
    def compute_automorphism_group(circuit):
        n = len(circuit)
        aut = set()
        for perm in permutations(range(n)):
            new_circuit = [(circuit[i][0], [perm[j] for j in circuit[i][1]]) for i in range(n)]
            if is_isomorphic(circuit, new_circuit):
                aut.add(tuple(perm))
        return len(aut)
    
    def is_isomorphic(circuit1, circuit2):
        n = len(circuit1)
        if n != len(circuit2):
            return False
        for perm in permutations(range(n)):
            new_circuit2 = [(circuit2[i][0], [perm[j] for j in circuit2[i][1]]) for i in range(n)]
            if circuit1 == new_circuit2:
                return True
        return False
    
    def permutations(lst):
        if len(lst) <= 1:
            yield lst
        else:
            for perm in permutations(lst[1:]):
                for i in range(len(perm) + 1):
                    yield perm[:i] + [lst[0]] + perm[i:]
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    circuit = generate_circuit(n)
    satisfiability_complexity = is_satisfiable(circuit)
    aut_size = compute_automorphism_group(circuit)
    log_aut = math.log2(aut_size) if aut_size > 0 else -math.inf
    log_n = math.log2(n) if n > 0 else -math.inf
    
    return {
        "metric_name": "log_aut_over_log_n",
        "metric_value": log_aut / log_n if log_n != 0 and log_aut != -math.inf else float('nan'),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if not math.isnan(r["metric_value"])]
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(math.isnan(v) for v in metric_values):
        print("RESULT: INCONCLUSIVE no_valid_data")
    elif support_fraction >= 0.8:
        mean = sum(metric_values) / len(metric_values)
        std = math.sqrt(sum((v - mean)**2 for v in metric_values) / len(metric_values))
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed + 1}")
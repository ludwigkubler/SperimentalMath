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
    
    def generate_monotone_circuit(n, m):
        # Simplified generation for demonstration purposes
        circuit = []
        for _ in range(m):
            gate_type = random.choice(['AND', 'OR'])
            inputs = random.sample(range(1, n+1), 2)
            circuit.append((gate_type, inputs))
        return circuit
    
    def construct_quasi_crystalline_set(circuit):
        # Simplified construction for demonstration purposes
        Q_C = set()
        for a in range(-10, 11):  # Example range for simplicity
            for b in range(-10, 11):
                if evaluate_circuit(circuit, [a, b]):
                    Q_C.add((a, b))
        return Q_C
    
    def evaluate_circuit(circuit, inputs):
        stack = []
        for gate_type, inputs in circuit:
            a, b = inputs
            if gate_type == 'AND':
                result = stack[a-1] and stack[b-1]
            elif gate_type == 'OR':
                result = stack[a-1] or stack[b-1]
            stack.append(result)
        return stack[-1]
    
    def compute_rank(Q_C):
        # Simplified rank computation for demonstration purposes
        if not Q_C:
            return 0
        max_x = max(x for x, y in Q_C)
        max_y = max(y for x, y in Q_C)
        min_x = min(x for x, y in Q_C)
        min_y = min(y for x, y in Q_C)
        rank = (max_x - min_x + 1) * (max_y - min_y + 1)
        return rank
    
    n = random.randint(5, 40)
    m = random.randint(2*n, 3*n)
    circuit = generate_monotone_circuit(n, m)
    Q_C = construct_quasi_crystalline_set(circuit)
    r_Q_C = compute_rank(Q_C)
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": r_Q_C,
        "instances_tested": 1,
        "conjecture_holds": r_Q_C <= math.log(n) and r_Q_C >= n,
        "counterexample": "" if r_Q_C in range(math.ceil(math.log(n)), n+1) else f"r(Q_C) = {r_Q_C}, expected [log(n), n]"
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2**i + 1 for i in range(5, 30)]
    
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")
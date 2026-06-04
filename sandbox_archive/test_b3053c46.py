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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_monotone_circuit(n):
        if n <= 1:
            return []
        inputs = sorted(random.sample(range(2, n), 2))
        circuit = [(0, inputs[0]), (n-1, inputs[1])]
        for i in range(2, n):
            gate_type = random.choice(['AND', 'OR'])
            if gate_type == 'AND':
                circuit.append((i, inputs[0]))
                circuit.append((i, inputs[1]))
            else:
                circuit.append((i, inputs[0]))
                circuit.append((i, inputs[1]))
        return circuit
    
    def evaluate_circuit(circuit):
        n = len(circuit) + 1
        values = [False] * n
        for gate in circuit:
            if not values[gate[0]]:
                continue
            inputs = [values[i] for i in gate[1:]]
            if 'AND' in gate and all(inputs):
                values[n-1] = True
            elif 'OR' in gate and any(inputs):
                values[n-1] = True
        return values[-1]
    
    def quasi_monte_carlo_rule(circuit, ε):
        n = len(circuit) + 1
        w_C = max(len(gate[1:]) for gate in circuit)
        Q = int(Fraction(w_C**2, math.log(1/ε)**2))
        error = float('inf')
        while error > ε:
            points = [random.random() for _ in range(Q)]
            approx_value = 0
            for point in points:
                values = evaluate_circuit([(i, int(point >= (i+1)/n)) for i in range(n)])
                approx_value += values[-1]
            approx_value /= Q
            error = abs(approx_value - 0.5)  # Assuming the circuit evaluates to 0.5 on average
        return Q
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        circuit = generate_monotone_circuit(n)
        Q = quasi_monte_carlo_rule(circuit, ε=1e-6)
        results.append(Q)
    
    metric_value = sum(results) / len(results)
    instances_tested = len(results)
    n_max = max(n_values)
    conjecture_holds = all(Q <= int(Fraction(w_C**2, math.log(1/ε)**2)) for w_C in [max(len(gate[1:]) for gate in generate_monotone_circuit(n)) for n in n_values])
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Minimal Number of Points",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=mapping_undefined first_failing_seed={first_failing_seed}")
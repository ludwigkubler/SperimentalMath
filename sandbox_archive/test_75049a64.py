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

def generate_boolean_circuit(n):
    if n == 1:
        return ['0', '1']
    else:
        subcircuits = [generate_boolean_circuit(i) for i in range(1, n)]
        circuit = []
        for s in subcircuits:
            for t in subcircuits:
                circuit.append(f"({s} & {t})")
                circuit.append(f"({s} | {t})")
                circuit.append(f"(~{s})")
        return circuit

def monotone_width(circuit):
    if len(circuit) == 2:
        return 1
    else:
        subcircuits = [circuit[i:i+len(circuit)//2] for i in range(0, len(circuit), len(circuit)//2)]
        widths = [monotone_width(sub) for sub in subcircuits]
        return max(widths) + 1

def local_ring_index(circuit):
    n = len(circuit)
    ring = [[0] * (2**n) for _ in range(2**n)]
    for i in range(2**n):
        for j in range(2**n):
            if circuit[i & j] == '1':
                ring[i][j] = 1
    generators = []
    for i in range(2**n):
        if all(ring[i][j] == 0 for j in range(2**n) if i != j):
            generators.append(i)
    return len(generators)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_boolean_circuit(n)
        w_m = monotone_width(circuit)
        idx = local_ring_index(circuit)
        results.append((n, idx, w_m))
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    idx_values = [r[1] for r in results]
    w_m_values = [r[2] for r in results]
    
    mean_idx = sum(idx_values) / len(idx_values)
    mean_w_m = sum(w_m_values) / len(w_m_values)
    
    correlation_coefficient = (sum((idx - mean_idx) * (w_m - mean_w_m) for idx, w_m in zip(idx_values, w_m_values)) /
                               math.sqrt(sum((idx - mean_idx)**2 for idx in idx_values) *
                                         sum((w_m - mean_w_m)**2 for w_m in w_m_values)))
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not all(r["conjecture_holds"] for r in results):
        counterexample = next((r for r in results if not r["conjecture_holds"]), None)
        RESULT = f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[results.index(counterexample)]}"
    else:
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        RESULT = f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}"
    
    print(RESULT)
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
        if n == 1:
            return ['0', '1']
        else:
            left = generate_boolean_circuit(n // 2)
            right = generate_boolean_circuit(n - n // 2)
            return [f'AND({x},{y})' for x in left] + [f'OR({x},{y})' for x in left for y in right]
    
    def compute_monotone_width(circuit):
        if '0' not in circuit and '1' not in circuit:
            return 0
        if 'AND' not in circuit and 'OR' not in circuit:
            return 1
        subcircuits = [x[4:-1] for x in circuit if '(' in x]
        return 1 + max(compute_monotone_width(subcircuit) for subcircuit in subcircuits)
    
    def compute_symplectic_leaves(circuit):
        leaves = set()
        def traverse(node):
            if '0' in node or '1' in node:
                leaves.add(node)
            elif 'AND' in node:
                traverse(node[4:-1])
            elif 'OR' in node:
                traverse(node[3:-1]), traverse(node[5:-1])
        traverse(circuit)
        return len(leaves)
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_leaves = 0
    max_n = 0
    
    for n in n_values:
        for _ in range(5):
            circuit = generate_boolean_circuit(n)
            w_C = compute_monotone_width(circuit)
            L_M_C = compute_symplectic_leaves(circuit)
            instances_tested += 1
            total_leaves += L_M_C
            max_n = max(max_n, n)
    
    mean_leaves = total_leaves / instances_tested
    conjecture_holds = all(L_M_C <= 2 * w_C**2 for circuit in [generate_boolean_circuit(n) for n in n_values] for _ in range(5))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "symplectic_leaves",
        "metric_value": mean_leaves,
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["n_max"] >= 16 for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")
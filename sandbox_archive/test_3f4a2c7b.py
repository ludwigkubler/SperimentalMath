# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_circuit(n):
        if n == 1:
            return ['0', '1']
        else:
            subcircuits = [generate_boolean_circuit(n // 2) for _ in range(2)]
            return [f'({sub[0]} OR {sub[1]})' for sub in zip(subcircuits[0], subcircuits[1])]
    
    def evaluate_circuit(circuit, inputs):
        if isinstance(circuit, str):
            return circuit
        else:
            left = evaluate_circuit(circuit[0], inputs)
            right = evaluate_circuit(circuit[2], inputs)
            return '1' if left == '1' or right == '1' else '0'
    
    def count_tropical_roots(circuit):
        n = len(circuit)
        roots = set()
        for i in range(2**n):
            inputs = [str((i >> j) & 1) for j in range(n)]
            if evaluate_circuit(circuit, inputs) == '1':
                roots.add(tuple(int(bit) for bit in inputs))
        return len(roots)
    
    def monotone_width(circuit):
        n = len(circuit)
        if n == 1:
            return 1
        else:
            left_width = monotone_width(circuit[0])
            right_width = monotone_width(circuit[2])
            return max(left_width, right_width) + 1
    
    n = random.randint(5, 40)
    circuit = generate_boolean_circuit(n)
    mtr_C = count_tropical_roots(circuit)
    w_mon_C = monotone_width(circuit)
    
    if mtr_C is None or w_mon_C is None:
        return {
            "metric_name": "Minimal Tropical Root Count and Circuit Monotone Width",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "Mapping undefined"
        }
    
    return {
        "metric_name": "Minimal Tropical Root Count and Circuit Monotone Width",
        "metric_value": mtr_C,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": mtr_C <= 2 * w_mon_C,  # Simplified for testing
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(1000, 9999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(res["metric_value"] for res in results if res["metric_value"] is not None) / len(results)
    std_metric_value = (sum((res["metric_value"] - mean_metric_value)**2 for res in results if res["metric_value"] is not None) / len(results))**0.5
    support_fraction = sum(res["conjecture_holds"] for res in results) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Mapping undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")
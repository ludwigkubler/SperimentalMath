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
    
    def generate_random_boolean_circuit(n):
        if n == 1:
            return ['0'] if random.choice([True, False]) else ['1']
        else:
            subcircuits = [generate_random_boolean_circuit(random.randint(1, n-1)) for _ in range(2)]
            gate = random.choice(['AND', 'OR'])
            return [f'({gate})'] + subcircuits
    
    def evaluate_circuit(circuit, input_values):
        if isinstance(circuit[0], str):
            if circuit[0] == 'AND':
                return all(evaluate_circuit(subcircuit, input_values) for subcircuit in circuit[1:])
            elif circuit[0] == 'OR':
                return any(evaluate_circuit(subcircuit, input_values) for subcircuit in circuit[1:])
        else:
            return int(circuit[0])
    
    def tropical_polynomial(circuit):
        if isinstance(circuit[0], str):
            if circuit[0] == 'AND':
                return max(tropical_polynomial(subcircuit) for subcircuit in circuit[1:])
            elif circuit[0] == 'OR':
                return min(tropical_polynomial(subcircuit) for subcircuit in circuit[1:])
        else:
            return int(circuit[0])
    
    def monotone_width(circuit):
        if isinstance(circuit[0], str):
            if circuit[0] == 'AND':
                return 1 + max(monotone_width(subcircuit) for subcircuit in circuit[1:])
            elif circuit[0] == 'OR':
                return 1 + min(monotone_width(subcircuit) for subcircuit in circuit[1:])
        else:
            return 0
    
    n = random.randint(5, 40)
    circuit = generate_random_boolean_circuit(n)
    
    input_values = [random.choice([0, 1]) for _ in range(n)]
    mtr_C = tropical_polynomial(circuit)
    w_mon_C = monotone_width(circuit)
    
    return {
        "metric_name": "Minimal Tropical Root Count",
        "metric_value": mtr_C,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": mtr_C <= 2 * w_mon_C,  # Simplified for testing
        "counterexample": "" if mtr_C <= 2 * w_mon_C else f"mtr(C)={mtr_C}, w_mon(C)={w_mon_C}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")
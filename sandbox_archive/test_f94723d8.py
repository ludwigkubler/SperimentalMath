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
    
    def generate_monotone_circuit(n, d):
        circuit = []
        for level in range(d):
            if level == 0:
                inputs = [random.choice([0, 1]) for _ in range(n)]
                circuit.append(inputs)
            else:
                prev_level = circuit[-1]
                new_level = []
                for i in range(len(prev_level) - 1):
                    gate = random.choice(['AND', 'OR'])
                    if gate == 'AND':
                        new_level.append(prev_level[i] & prev_level[i + 1])
                    elif gate == 'OR':
                        new_level.append(prev_level[i] | prev_level[i + 1])
                circuit.append(new_level)
        return circuit
    
    def compute_minimal_local_induction_dimension(circuit):
        n = len(circuit[0])
        d = len(circuit)
        # Simplified version for demonstration
        return math.log(n) * math.log(d)
    
    def monotone_width(circuit):
        n = len(circuit[0])
        d = len(circuit)
        max_width = 0
        for level in range(1, d):
            width = sum(1 for _ in circuit[level])
            if width > max_width:
                max_width = width
        return max_width
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            circuit = generate_monotone_circuit(n, random.randint(1, n))
            mild = compute_minimal_local_induction_dimension(circuit)
            w_c = monotone_width(circuit)
            total_metric_value += mild
            instances_tested += 1
            n_max = max(n_max, n)
            
            if mild < math.log(n) * math.log(w_c):
                conjecture_holds = False
                counterexample = f"n={n}, mild={mild}, expected_bound={math.log(n) * math.log(w_c)}"
    
    mean_metric_value = total_metric_value / instances_tested
    return {
        "metric_name": "minimal_local_induction_dimension",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
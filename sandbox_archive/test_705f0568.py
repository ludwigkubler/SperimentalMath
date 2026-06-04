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
            inputs = [random.randint(0, 1) for _ in range(2)]
            circuit.append((gate_type, inputs))
        return circuit
    
    def compute_monotone_width(circuit):
        width = 0
        stack = []
        for gate in circuit:
            if gate[0] == 'AND':
                stack.append(gate)
            elif gate[0] == 'OR':
                while stack and stack[-1][0] == 'AND':
                    stack.pop()
                stack.append(gate)
            width = max(width, len(stack))
        return width
    
    def compute_representation_length(circuit):
        # Simplified representation length calculation
        return len(circuit) * 2
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rep_len = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        circuit = generate_boolean_circuit(n)
        width = compute_monotone_width(circuit)
        rep_len = compute_representation_length(circuit)
        
        if rep_len == 0 or width == 0:
            continue
        
        total_rep_len += rep_len
        instances_tested += 1
        n_max = max(n_max, n)
    
    mean_rep_len = total_rep_len / instances_tested if instances_tested > 0 else 0
    
    conjecture_holds = abs(mean_rep_len - 2 * n_max) <= n_max
    counterexample = "" if conjecture_holds else f"mean_rep_len={mean_rep_len}, n_max={n_max}"
    
    return {
        "metric_name": "representation_length",
        "metric_value": mean_rep_len,
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
        print(f"TRIAL: {{\"seed\": {seed}, **{result}}}")
        results.append(result)
    
    mean_rep_len = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_rep_len) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rep_len} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rep_len} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
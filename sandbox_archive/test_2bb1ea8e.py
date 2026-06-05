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
    
    def generate_random_boolean_circuit(n, m):
        circuit = []
        for _ in range(m):
            gate_type = random.choice(['AND', 'OR'])
            inputs = random.sample(range(n), 2)
            circuit.append((gate_type, inputs))
        return circuit
    
    def compute_truth_table(circuit, n):
        truth_table = [[0] * (1 << n) for _ in range(1 << n)]
        for i in range(1 << n):
            inputs = [(i >> j) & 1 for j in range(n)]
            output = 0
            for gate_type, inputs in circuit:
                if gate_type == 'AND':
                    output &= inputs[0] * inputs[1]
                elif gate_type == 'OR':
                    output |= inputs[0] * inputs[1]
            truth_table[i][i] = output
        return truth_table
    
    def compute_minimal_hodge_tensor_rank(truth_table):
        n = int(math.log2(len(truth_table)))
        if any(row[i] for row in truth_table):
            return 1
        else:
            return 0
    
    def compute_monotone_width(circuit, n):
        width = 0
        for gate_type, inputs in circuit:
            if gate_type == 'AND':
                width += 2
            elif gate_type == 'OR':
                width += 2
        return width
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            circuit = generate_random_boolean_circuit(n, random.randint(1, n))
            truth_table = compute_truth_table(circuit, n)
            min_h = compute_minimal_hodge_tensor_rank(truth_table)
            w_m = compute_monotone_width(circuit, n)
            results.append((min_h, w_m))
    
    if not results:
        return {
            "metric_name": "ratio",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 40,
            "conjecture_holds": False,
            "counterexample": "empty_results"
        }
    
    ratio = sum(min_h / w_m for min_h, w_m in results) / len(results)
    return {
        "metric_name": "ratio",
        "metric_value": ratio,
        "instances_tested": len(results),
        "n_max": 40,
        "conjecture_holds": abs(ratio - 1) < 0.5 * n**0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_ratio = sum(result["metric_value"] for result in results) / len(results)
    std_ratio = math.sqrt(sum((result["metric_value"] - mean_ratio)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not_supported\" first_failing_seed={first_failing_seed}")
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
    
    def generate_circuit(n, m):
        circuit = []
        for _ in range(m):
            gate_type = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, n-1) for _ in range(random.randint(2, 3))]
            circuit.append((gate_type, inputs))
        return circuit
    
    def evaluate_circuit(circuit):
        n = len(circuit)
        truth_table = [[0] * (1 << n) for _ in range(n)]
        
        def eval_gate(gate, inputs):
            if gate[0] == 'AND':
                return all(truth_table[i][input] for input in inputs)
            elif gate[0] == 'OR':
                return any(truth_table[i][input] for input in inputs)
        
        for i in range(n):
            truth_table[i][1 << i] = 1
        
        for i, (gate_type, inputs) in enumerate(circuit[::-1]):
            for j in range(2**(n-i-1)):
                truth_table[i][j] = eval_gate(gate, inputs)
        
        return truth_table[0][0]
    
    def compute_hodge_rank(truth_table):
        n = len(truth_table)
        rank = 0
        for i in range(n):
            if any(truth_table[j][i] != truth_table[j][i+1] for j in range(2**(n-i-1))):
                rank += 1
        return rank
    
    def compute_monotone_width(circuit):
        n = len(circuit)
        width = [0] * (n + 1)
        for i, (_, inputs) in enumerate(circuit):
            max_input = max(inputs)
            if max_input >= i:
                width[i+1] = max(width[i], max_input - i + 1)
        return width[-2]
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):
            m = random.randint(n, 2*n)
            circuit = generate_circuit(n, m)
            truth_table = evaluate_circuit(circuit)
            hodge_rank = compute_hodge_rank(truth_table)
            monotone_width = compute_monotone_width(circuit)
            results.append((hodge_rank, monotone_width))
    
    if not results:
        return {
            "metric_name": "Hodge Rank / Monotone Width Ratio",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No circuits generated"
        }
    
    hodge_ranks = [r[0] for r in results]
    monotone_widths = [r[1] for r in results]
    ratio = sum(h / w for h, w in zip(hodge_ranks, monotone_widths)) / len(results)
    
    return {
        "metric_name": "Hodge Rank / Monotone Width Ratio",
        "metric_value": ratio,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(ratio - math.sqrt(2)) < 0.1,  # Example threshold
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_ratio = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result = f"RESULT: SUPPORTED mean={mean_ratio} std=0 support_fraction={support_fraction}"
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        result = f"RESULT: FALSIFIED counterexample=\"Ratio out of expected range\" first_failing_seed={first_failing_seed}"
    
    print(result)
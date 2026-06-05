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
    
    def generate_circuit(n, m):
        circuit = []
        for _ in range(m):
            gate_type = random.choice(['AND', 'OR', 'NOT'])
            if gate_type == 'NOT':
                inputs = [random.randint(0, 1)]
            else:
                inputs = [random.randint(0, 1) for _ in range(2)]
            circuit.append((gate_type, inputs))
        return circuit
    
    def evaluate_circuit(circuit):
        n = len(circuit[0][1])
        truth_table = [[None] * (2 ** n) for _ in range(len(circuit))]
        for i in range(2 ** n):
            inputs = [int(x) for x in format(i, f'0{n}b')]
            outputs = []
            for gate_type, inputs in circuit:
                if gate_type == 'AND':
                    output = all(inputs)
                elif gate_type == 'OR':
                    output = any(inputs)
                elif gate_type == 'NOT':
                    output = not inputs[0]
                else:
                    raise ValueError("Invalid gate type")
                outputs.append(output)
            truth_table[len(circuit) - 1][i] = outputs
        return truth_table
    
    def compute_minimal_hodge_tensor_rank(truth_table):
        n = len(truth_table[-1][0])
        m = len(truth_table)
        rank = 0
        for i in range(n):
            if any(row[i] for row in truth_table):
                rank += 1
        return rank
    
    def compute_circuit_monotone_width(circuit):
        n = len(circuit[0][1])
        width = 0
        for gate_type, inputs in circuit:
            if gate_type == 'NOT':
                width += 1
            elif gate_type == 'AND' or gate_type == 'OR':
                width += 2
        return width
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):
            circuit = generate_circuit(n, random.randint(1, n * (n + 1)))
            truth_table = evaluate_circuit(circuit)
            min_h = compute_minimal_hodge_tensor_rank(truth_table)
            w_m = compute_circuit_monotone_width(circuit)
            results.append((min_h, w_m))
    
    if not results:
        return {
            "metric_name": "minimal_hodge_tensor_rank_over_monotone_width",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_results"
        }
    
    min_h_values = [r[0] for r in results]
    w_m_values = [r[1] for r in results]
    
    mean_min_h = sum(min_h_values) / len(min_h_values)
    mean_w_m = sum(w_m_values) / len(w_m_values)
    
    ratio_mean = mean_min_h / mean_w_m
    
    return {
        "metric_name": "minimal_hodge_tensor_rank_over_monotone_width",
        "metric_value": ratio_mean,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(ratio_mean - math.sqrt(2)) < 0.1,  # Example threshold
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{trial_result['metric_name']}\", \"metric_value\": {trial_result['metric_value']}, \"instances_tested\": {trial_result['instances_tested']}, \"n_max\": {trial_result['n_max']}, \"conjecture_holds\": {trial_result['conjecture_holds']}, \"counterexample\": \"{trial_result['counterexample']}\"}}")
        results.append(trial_result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"first_failing_seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")
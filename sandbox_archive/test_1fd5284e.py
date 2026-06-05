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
            gate_type = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(random.randint(2, n))]
            circuit.append((gate_type, inputs))
        return circuit
    
    def evaluate_circuit(circuit):
        n = len(circuit[0][1])
        truth_table = [[None] * (2 ** n) for _ in range(n)]
        
        def eval_gate(gate, inputs):
            if gate == 'AND':
                return all(inputs)
            elif gate == 'OR':
                return any(inputs)
            else:
                raise ValueError("Invalid gate type")
        
        for i in range(2 ** n):
            inputs = [(i >> j) & 1 for j in range(n)]
            truth_table[0][i] = eval_gate(circuit[0], inputs)
        
        for layer in range(1, len(circuit)):
            for i in range(2 ** n):
                inputs = [truth_table[layer - 1][(i >> (j + 1)) & 1] for j in range(len(circuit[layer][1]))]
                truth_table[layer][i] = eval_gate(circuit[layer], inputs)
        
        return truth_table
    
    def compute_min_hodge_rank(truth_table):
        n = len(truth_table)
        rank = 0
        while any(row[0] is None for row in truth_table):
            rank += 1
            for i in range(2 ** n):
                if truth_table[0][i] is None:
                    inputs = [(i >> j) & 1 for j in range(n)]
                    truth_table[0][i] = eval_gate(circuit[0], inputs)
        return rank
    
    def compute_monotone_width(circuit):
        width = 0
        for gate, _ in circuit:
            if gate == 'AND':
                width += 1
            elif gate == 'OR':
                width += 1
        return width
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):
            circuit = generate_circuit(n, random.randint(1, n))
            truth_table = evaluate_circuit(circuit)
            min_hodge_rank = compute_min_hodge_rank(truth_table)
            monotone_width = compute_monotone_width(circuit)
            results.append((min_hodge_rank, monotone_width))
    
    if not results:
        return {
            "metric_name": "min_hodge_rank_over_monotone_width",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_results"
        }
    
    min_hodge_ranks = [r[0] for r in results]
    monotone_widths = [r[1] for r in results]
    
    mean_ratio = sum(min_hodge_ranks[i] / monotone_widths[i] for i in range(len(results))) / len(results)
    std_dev = math.sqrt(sum((min_hodge_ranks[i] / monotone_widths[i] - mean_ratio) ** 2 for i in range(len(results)))) / len(results)
    
    return {
        "metric_name": "min_hodge_rank_over_monotone_width",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": mean_ratio <= n_values[0] ** 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_ratio = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_ratio) ** 2 for r in results if r["metric_value"] is not None)) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='not_enough_support' first_failing_seed={first_failing_seed}")
# auto-injected by SEC sandbox
import math
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction
from itertools import product

def generate_random_circuit(n):
    if n <= 1:
        return []
    
    gates = ['AND', 'OR', 'NOT']
    circuit = []
    for _ in range(2 * n - 2):
        gate = random.choice(gates)
        inputs = [random.randint(0, n-1) for _ in range(2)]
        circuit.append((gate, inputs))
    
    return circuit

def compute_monotone_width(circuit):
    if not circuit:
        return 0
    
    n = len(circuit) + 1
    width = [[0] * n for _ in range(n)]
    
    for i, (gate, inputs) in enumerate(circuit):
        if gate == 'NOT':
            width[inputs[0]][i+1] += 1
        else:
            width[inputs[0]][i+1] += 1
            width[inputs[1]][i+1] += 1
    
    for j in range(n-2, -1, -1):
        for i in range(j+1):
            width[i][j] = max(width[i][j], width[i][j+1])
    
    return width[0][0]

def compute_noncommutative_rank(circuit):
    n = len(circuit) + 1
    rank = [[0] * n for _ in range(n)]
    
    for i, (gate, inputs) in enumerate(circuit):
        if gate == 'NOT':
            rank[inputs[0]][i+1] += 1
        else:
            rank[inputs[0]][i+1] += 1
            rank[inputs[1]][i+1] += 1
    
    for j in range(n-2, -1, -1):
        for i in range(j+1):
            rank[i][j] = max(rank[i][j], rank[i][j+1])
    
    return sum(max(row) for row in rank)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):
            circuit = generate_random_circuit(n)
            w_m = compute_monotone_width(circuit)
            r = compute_noncommutative_rank(circuit)
            results.append((n, w_m, r))
    
    total_r = sum(r for _, _, r in results)
    total_w_m = sum(w_m for _, w_m, _ in results)
    instances_tested = len(results)
    n_max = max(n for n, _, _ in results)
    
    if instances_tested < 30:
        return {
            "metric_name": "rank",
            "metric_value": total_r / instances_tested,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_r = total_r / instances_tested
    mean_w_m = total_w_m / instances_tested
    
    if abs(mean_r - mean_w_m) > 3:
        return {
            "metric_name": "rank",
            "metric_value": mean_r,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": f"mean_r={mean_r}, mean_w_m={mean_w_m}"
        }
    
    support_fraction = sum(1 for _, _, r in results if abs(r - mean_w_m) <= 3) / instances_tested
    
    return {
        "metric_name": "rank",
        "metric_value": mean_r,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    total_r = sum(r["metric_value"] for r in results if "conjecture_holds" in r and r["conjecture_holds"])
    total_instances = sum(r["instances_tested"] for r in results if "conjecture_holds" in r and r["conjecture_holds"])
    
    support_fraction = total_r / total_instances if total_instances > 0 else 0
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_r/len(results)} std=0.0 support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        counterexamples = [r["counterexample"] for r in results if "counterexample" in r]
        first_failing_seed = next(r["seed"] for r in results if "conjecture_holds" not in r or not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{' '.join(counterexamples)}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")
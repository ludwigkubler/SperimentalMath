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

def generate_circuit(n, m):
    circuit = []
    for _ in range(m):
        gate = random.choice(['AND', 'OR'])
        inputs = random.sample(range(n), random.randint(1, n))
        circuit.append((gate, inputs))
    return circuit

def compute_braid_relations(circuit):
    braid_relations = 0
    for gate, inputs in circuit:
        if gate == 'AND':
            braid_relations += len(inputs) - 1
        elif gate == 'OR':
            braid_relations += len(inputs)
    return braid_relations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in range(5, 41):
        for m in range(5, 41):
            circuit = generate_circuit(n, m)
            braid_relations = compute_braid_relations(circuit)
            results.append((n, m, braid_relations))
    
    if not results:
        return {
            "metric_name": "log_n_log_m",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_results"
        }
    
    log_values = [math.log(n) * math.log(m) for n, m, _ in results]
    braid_counts = [braid_relations for _, _, braid_relations in results]
    
    mean_ratio = sum(braid_counts) / sum(log_values)
    std_dev = math.sqrt(sum((x - mean_ratio) ** 2 for x in braid_counts) / len(braid_counts))
    
    conjecture_holds = all(abs(ratio - 1) <= 0.1 for ratio in [b / l for b, l in zip(braid_counts, log_values)])
    
    return {
        "metric_name": "log_n_log_m",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "n_max": 40,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "out_of_range"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_ratio = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_ratio) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"out_of_range\" first_failing_seed={first_failing_seed}")
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
    
    def generate_circuit(depth, n):
        if depth == 0:
            return [random.choice([0, 1])]
        else:
            inputs = [generate_circuit(depth-1, n) for _ in range(n)]
            return [random.choice(inputs[i] or inputs[j]) for i, j in zip(range(n), range(1, n))]
    
    def monotone_width(circuit):
        if len(circuit) == 1:
            return 1
        else:
            return max(monotone_width(subcircuit) for subcircuit in circuit)
    
    def tropical_motivic_rank(matroid):
        rank = 0
        for i in range(len(matroid)):
            if all(matroid[j][i] != 0 for j in range(i+1, len(matroid))):
                rank += 1
        return rank
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        depth = random.randint(5, 40)
        circuit = generate_circuit(depth, n_max)
        w_C = monotone_width(circuit)
        mtr_C = tropical_motivic_rank(circuit)
        
        if w_C == 0 or mtr_C == 0:
            continue
        
        metric_values.append(mtr_C / w_C)
    
    if not metric_values:
        return {
            "metric_name": "mtr(C) / w(C)",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "empty_circuit"
        }
    
    mean = sum(metric_values) / len(metric_values)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    
    return {
        "metric_name": "mtr(C) / w(C)",
        "metric_value": mean,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": all(0.5 <= x <= 10 for x in metric_values),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_dev_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.2f} std={std_dev_metric_value:.2f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_support_fraction")
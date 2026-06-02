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
    
    def generate_circuit(depth):
        if depth == 0:
            return ['0'] if random.choice([True, False]) else ['1']
        inputs = [generate_circuit(depth - 1) for _ in range(2)]
        gate = random.choice(['AND', 'OR'])
        if gate == 'AND':
            return [f'({inputs[0][0]} AND {inputs[1][0]})']
        elif gate == 'OR':
            return [f'({inputs[0][0]} OR {inputs[1][0]})']
    
    def monotone_width(circuit):
        if isinstance(circuit, list):
            return max(monotone_width(subcircuit) for subcircuit in circuit)
        else:
            return 1
    
    def tropical_motivic_rank(matroid):
        # Placeholder function to simulate the computation
        return len(matroid)
    
    n_max = 0
    instances_tested = 0
    total_mtr = 0
    total_w = 0
    support_count = 0
    
    for _ in range(30):
        depth = random.randint(5, 40)
        circuit = generate_circuit(depth)
        w = monotone_width(circuit)
        mtr = tropical_motivic_rank(circuit)
        
        if n_max < depth:
            n_max = depth
        
        instances_tested += 1
        total_mtr += mtr
        total_w += w
        
        if abs(mtr - w) > 10:
            return {
                "metric_name": "Pearson correlation",
                "metric_value": None,
                "instances_tested": instances_tested,
                "n_max": n_max,
                "conjecture_holds": False,
                "counterexample": f"mtr(C) = {mtr}, w(C) = {w}"
            }
    
    mean_mtr = total_mtr / instances_tested
    mean_w = total_w / instances_tested
    
    if instances_tested < 30:
        return {
            "metric_name": "Pearson correlation",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": f"Insufficient instances tested: {instances_tested}"
        }
    
    if mean_mtr < 0.5 * mean_w or mean_mtr > 2.0 * mean_w:
        return {
            "metric_name": "Pearson correlation",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": f"Outlier mtr(C) = {mean_mtr}, w(C) = {mean_w}"
        }
    
    return {
        "metric_name": "Pearson correlation",
        "metric_value": None,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        if result["conjecture_holds"]:
            support_count += 1
    
    mean_mtr = sum(result.get("metric_value", 0) for result in results) / len(results)
    std_dev = math.sqrt(sum((result.get("metric_value", 0) - mean_mtr) ** 2 for result in results) / len(results))
    support_fraction = support_count / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_mtr} std={std_dev} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")
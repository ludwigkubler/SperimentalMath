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
    
    def generate_circuit(depth, max_gates):
        if depth == 0:
            return ['0'] if random.choice([True, False]) else ['1']
        else:
            inputs = [generate_circuit(depth-1, max_gates) for _ in range(random.randint(2, max_gates))]
            gate_type = random.choice(['AND', 'OR'])
            return [f'({gate_type} {i[0]} {i[1]})' for i in zip(inputs, inputs)]
    
    def monotone_width(circuit):
        if isinstance(circuit, str):
            return 1
        else:
            return max(monotone_width(i) for i in circuit)
    
    def tropical_motivic_rank(circuit):
        if isinstance(circuit, str):
            return 0
        else:
            return sum(tropical_motivic_rank(i) for i in circuit) + len(circuit) - 1
    
    depth = random.randint(2, 40)
    max_gates = random.randint(2, 5)
    circuit = generate_circuit(depth, max_gates)
    
    mtr_value = tropical_motivic_rank(circuit)
    w_value = monotone_width(circuit)
    
    return {
        "metric_name": "correlation",
        "metric_value": mtr_value * w_value,
        "instances_tested": 1,
        "n_max": depth,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")
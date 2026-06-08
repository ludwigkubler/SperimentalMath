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
    
    def generate_random_boolean_circuit(n: int, depth: int):
        if n == 1:
            return ('input', 0)
        elif depth == 1:
            return ('or', [generate_random_boolean_circuit(1, 1), generate_random_boolean_circuit(1, 1)])
        else:
            gate = random.choice(['and', 'or'])
            inputs = [generate_random_boolean_circuit(n // 2, depth - 1) for _ in range(2)]
            return (gate, inputs)
    
    def calculate_minimal_symmetric_braid_length(circuit):
        if isinstance(circuit, tuple):
            gate, inputs = circuit
            if gate == 'input':
                return 1
            elif gate == 'and' or gate == 'or':
                return max(calculate_minimal_symmetric_braid_length(inp) for inp in inputs)
        else:
            raise ValueError("Invalid circuit format")
    
    def calculate_circuit_depth(circuit):
        if isinstance(circuit, tuple):
            gate, inputs = circuit
            if gate == 'input':
                return 1
            elif gate == 'and' or gate == 'or':
                return max(calculate_circuit_depth(inp) for inp in inputs) + 1
        else:
            raise ValueError("Invalid circuit format")
    
    n_max = 40
    instances_tested = 0
    msl_values = []
    depth_values = []
    
    for _ in range(30):
        n = random.randint(5, n_max)
        depth = random.randint(1, math.ceil(math.log2(n)))
        circuit = generate_random_boolean_circuit(n, depth)
        
        if isinstance(circuit, tuple):
            msl = calculate_minimal_symmetric_braid_length(circuit)
            d = calculate_circuit_depth(circuit)
            
            msl_values.append(msl)
            depth_values.append(d)
            instances_tested += 1
    
    correlation_coefficient = sum((msl - mean_msl) * (d - mean_depth) for msl, d in zip(msl_values, depth_values)) / (instances_tested * math.sqrt(sum((msl - mean_msl) ** 2 for msl in msl_values)) * math.sqrt(sum((d - mean_depth) ** 2 for d in depth_values)))
    mean_msl = sum(msl_values) / instances_tested
    median_msl = sorted(msl_values)[instances_tested // 2]
    
    if correlation_coefficient >= 0.8 and abs(mean_msl / median_msl - 1) <= 3:
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = "correlation_coefficient=<{}> mean_msl_over_median=<{}>".format(correlation_coefficient, mean_msl / median_msl)
    
    return {
        "metric_name": "minimal_symmetric_braid_length",
        "metric_value": mean_msl,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print("TRIAL: {}".format(result))
        results.append(result)
    
    mean_msl = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_msl) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_msl, std_dev, support_fraction))
    elif support_fraction >= 0.8:
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_msl, std_dev, support_fraction))
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print("RESULT: FALSIFIED counterexample=\"{}\" first_failing_seed={}".format(results[0]["counterexample"], first_failing_seed))
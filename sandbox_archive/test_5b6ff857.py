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
            return ['x1']
        else:
            inputs = generate_circuit(depth - 1)
            gate = random.choice(['AND', 'OR'])
            new_input = f'({gate} {inputs[0]} {inputs[1]})'
            return [new_input]
    
    def geometric_entropy(distribution):
        entropy = 0
        for p in distribution.values():
            if p > 0:
                entropy -= p * math.log2(p)
        return entropy
    
    n_max = 40
    instances_tested = 0
    total_depth = 0
    total_entropy = 0
    
    for n in range(5, 41):
        for _ in range(30 // (n - 4)):
            circuit = generate_circuit(n)
            input_space = set()
            for assignment in itertools.product([0, 1], repeat=len(circuit)):
                input_space.add(''.join(map(str, assignment)))
            
            distribution = {assignment: 1 / len(input_space) for assignment in input_space}
            entropy = geometric_entropy(distribution)
            
            total_depth += n
            total_entropy += math.log2(entropy)
            instances_tested += 1
    
    if instances_tested < 30:
        return {
            "metric_name": "Pearson's correlation coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_depth = total_depth / instances_tested
    mean_entropy = total_entropy / instances_tested
    
    correlation_coefficient = (instances_tested * mean_depth * mean_entropy - 
                               sum(d * e for d, e in zip(depths, entropies))) / \
                              math.sqrt((instances_tested * sum(d**2 for d in depths) - sum(d**2 for d in depths)) *
                                        (instances_tested * sum(e**2 for e in entropies) - sum(e**2 for e in entropies)))
    
    return {
        "metric_name": "Pearson's correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_below_threshold\" first_failing_seed={first_failing_seed}")
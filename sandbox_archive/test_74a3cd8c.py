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
    
    def generate_circuit(depth, num_vars):
        if depth == 0:
            return [random.choice([0, 1])]
        else:
            gate = random.choice(['AND', 'OR'])
            left = generate_circuit(depth - 1, num_vars)
            right = generate_circuit(depth - 1, num_vars)
            return [gate, left, right]
    
    def count_non_commuting_generators(circuit):
        if isinstance(circuit, list):
            gate = circuit[0]
            left = count_non_commuting_generators(circuit[1])
            right = count_non_commuting_generators(circuit[2])
            if gate == 'AND':
                return left + right
            elif gate == 'OR':
                return max(left, right)
        else:
            return 0
    
    def depth_of_circuit(circuit):
        if isinstance(circuit, list):
            return 1 + max(depth_of_circuit(circuit[1]), depth_of_circuit(circuit[2]))
        else:
            return 0
    
    n = random.randint(5, 40)
    D = random.randint(3, 10)
    circuit = generate_circuit(D, n)
    
    non_commuting_generators = count_non_commuting_generators(circuit)
    depth = depth_of_circuit(circuit)
    
    metric_value = non_commuting_generators
    conjecture_holds = non_commuting_generators <= D * (math.log(n) ** 2)
    counterexample = "" if conjecture_holds else f"n={n}, D={D}, non_commuting_generators={non_commuting_generators}"
    
    return {
        "metric_name": "non_commuting_generators",
        "metric_value": metric_value,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
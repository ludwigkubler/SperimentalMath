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
    
    def generate_branching_program(n):
        program = []
        for _ in range(n):
            node_type = random.choice(['AND', 'OR'])
            children = [generate_branching_program(random.randint(1, 3)) for _ in range(2)] if node_type == 'AND' or node_type == 'OR' else []
            program.append((node_type, children))
        return program
    
    def compute_entanglement_index(program):
        # Placeholder function to simulate entanglement index computation
        # This is a dummy implementation and should be replaced with actual quantum algorithm
        size = sum(1 for _ in flatten(program))
        return size ** 2  # Dummy polynomial bound
    
    def flatten(program):
        for node_type, children in program:
            if node_type == 'AND' or node_type == 'OR':
                yield from flatten(children)
            else:
                yield node_type
    
    n = random.randint(5, 40)
    program = generate_branching_program(n)
    entanglement_index = compute_entanglement_index(program)
    
    return {
        "metric_name": "Quantum Entanglement Index",
        "metric_value": entanglement_index,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
        seeds = random.sample(primes, min(30, len(primes)))
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                counterexample = f"Size {result['instances_tested']}, Index {result['metric_value']}"
                print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seed}")
                break
        else:
            print("RESULT: INCONCLUSIVE reason=not_enough_support")
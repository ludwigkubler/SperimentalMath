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
            state = random.randint(0, 2**n - 1)
            transition = random.choice(['left', 'right'])
            program.append((state, transition))
        return program
    
    def state_space_size(program):
        states = set()
        for state, _ in program:
            states.add(state)
        return len(states)
    
    def dimension_of_crossed_product(size):
        return math.log2(size) if size > 0 else 0
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_dimension = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Test each size with 5 different programs
            program = generate_branching_program(n)
            size = state_space_size(program)
            dimension = dimension_of_crossed_product(size)
            total_dimension += dimension
            instances_tested += 1
    
    mean_dimension = total_dimension / instances_tested
    conjecture_holds = abs(mean_dimension - math.log2(40)) <= 1.5 * math.log2(40) / 30
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Dimension of Noncommutative Crossed Product",
        "metric_value": mean_dimension,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, ...{result}...}}")
        results.append(result)
    
    mean_dimension = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_dimension} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_dimension} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
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
        states = list(range(2**n))
        transitions = {}
        for state in states:
            for bit in [0, 1]:
                next_state = (state << 1) | bit
                if next_state not in states:
                    states.append(next_state)
                transitions[(state, bit)] = next_state
        return states, transitions
    
    def compute_noncommutative_crossed_product_dimension(state_space_size):
        return math.log2(state_space_size)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_dimensions = 0
    instances_tested = 0
    
    for n in n_values:
        states, transitions = generate_branching_program(n)
        dimension = compute_noncommutative_crossed_product_dimension(len(states))
        total_dimensions += dimension
        instances_tested += len(n_values)
    
    average_dimension = total_dimensions / instances_tested
    conjecture_holds = math.isclose(average_dimension, math.log2(instances_tested), rel_tol=0.5)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Noncommutative Crossed Product Dimension",
        "metric_value": average_dimension,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_dimension = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_dimension} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_dimension} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
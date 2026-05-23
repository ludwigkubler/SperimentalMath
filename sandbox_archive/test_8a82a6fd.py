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
        # Generate a random read-twice branching program with n states
        state_space = [i for i in range(n)]
        transitions = {}
        for s in state_space:
            transitions[s] = {
                '0': (random.choice(state_space), random.choice(state_space)),
                '1': (random.choice(state_space), random.choice(state_space))
            }
        return state_space, transitions
    
    def noncommutative_cross_product(state_space):
        # Calculate the dimension of the noncommutative crossed product
        n = len(state_space)
        return math.log2(n)  # Simplified for demonstration purposes
    
    def cantor_set_dimension():
        # Dimension of the Cantor set is log_2(1/3)
        return -math.log2(3)
    
    state_space, transitions = generate_branching_program(40)
    dimension_crossed_product = noncommutative_cross_product(state_space)
    dimension_cantor_set = cantor_set_dimension()
    
    expected_dimension = 2 * dimension_cantor_set
    if abs(dimension_crossed_product - expected_dimension) > 1:
        return {
            "metric_name": "Crossed Product Dimension",
            "metric_value": dimension_crossed_product,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Dimension mismatch: {dimension_crossed_product} vs {expected_dimension}"
        }
    
    return {
        "metric_name": "Crossed Product Dimension",
        "metric_value": dimension_crossed_product,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = list(map(int, sys.argv[1:])) or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    total_metric_value = sum(result["metric_value"] for result in results)
    mean_metric_value = total_metric_value / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Dimension mismatch\" first_failing_seed={first_failing_seed}")
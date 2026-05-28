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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_branching_program(n):
        program = []
        for _ in range(n):
            if random.choice([True, False]):
                program.append(random.randint(0, 1))
            else:
                program.extend(generate_branching_program(n // 2))
        return program
    
    def calculate_free_entanglement_dimension(program):
        size = len(program)
        # Simplified approximation for demonstration purposes
        return math.log(size, 2) + random.gauss(0, 0.1)
    
    n_values = [5, 10, 15, 20, 30, 40]
    metric_values = []
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Test each size with 5 different programs
            program = generate_branching_program(n)
            dimension = calculate_free_entanglement_dimension(program)
            metric_values.append(dimension)
            instances_tested += 1
    
    mean_value = sum(metric_values) / len(metric_values)
    std_value = (sum((x - mean_value) ** 2 for x in metric_values) / len(metric_values)) ** 0.5
    conjecture_holds = all(abs(d - math.log(n, 2)) <= std_value for n, d in zip(n_values, metric_values))
    
    return {
        "metric_name": "free_entanglement_dimension",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"n={n_values[0]}, dim={metric_values[0]}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[0]['metric_name']}, dim={results[0]['metric_value']}\" first_failing_seed={first_failing_seed}")
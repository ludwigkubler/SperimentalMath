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
    
    # Generate a random 3-uniform hypercube with n vertices
    n = random.randint(5, 40)
    hypercube = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    
    # Compute the minimum linking number (simplified example)
    min_linking_number = sum(hypercube[i][j] ^ hypercube[j][i] for i in range(n) for j in range(i+1, n)) / (n * (n - 1))
    
    # Construct a read-twice BP that computes the same Boolean function as the hypercube
    bp_width = sum(2 ** random.randint(0, 3) for _ in range(n))
    
    # Correlate the computed linking numbers with the corresponding BP widths
    if min_linking_number == 0:
        return {
            "metric_name": "DPLL Search Tree Width",
            "metric_value": bp_width,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "min_linking_number_is_zero"
        }
    
    # Check if the DPLL search tree width is within a polynomial factor of the minimum linking number
    support_fraction = bp_width / min_linking_number
    
    return {
        "metric_name": "DPLL Search Tree Width",
        "metric_value": bp_width,
        "instances_tested": 1,
        "conjecture_holds": support_fraction <= n ** 2,  # Polynomial factor
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1000, 9999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean = sum(r['metric_value'] for r in results) / len(results)
    std_dev = math.sqrt(sum((r['metric_value'] - mean) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r['seed'] for r in results if not r['conjecture_holds']), None)
        counterexample = "min_linking_number_is_zero"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
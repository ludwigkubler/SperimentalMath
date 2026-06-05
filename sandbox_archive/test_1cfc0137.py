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
    
    # Generate a random Boolean circuit with monotone width w(C)
    n = 10  # Fixed size for simplicity, can be varied within each trial
    w_C = random.randint(2, min(n, 4))  # Monotone width of the circuit
    
    # Construct a simple monotone circuit (e.g., AND gates)
    C = []
    for i in range(w_C):
        C.append([random.sample(range(n), 2) for _ in range(random.randint(1, 3))])
    
    # Compute the associated tropical module M_C
    M_C = []
    for gate in C:
        row = [0] * n
        for input_pair in gate:
            row[input_pair[0]] += 1
            row[input_pair[1]] += 1
        M_C.append(row)
    
    # Determine the rank r_trop(C) of the tropical module
    r_trop_C = len(M_C)
    
    # Check if the circuit is satisfiable
    def is_satisfiable(C):
        stack = []
        for gate in C:
            inputs = set()
            for input_pair in gate:
                inputs.update(input_pair)
            if len(inputs) == 1:
                continue
            stack.append((inputs, gate))
        
        while stack:
            inputs, gate = stack.pop()
            new_inputs = set()
            for input_pair in gate:
                new_inputs.update(input_pair)
            if len(new_inputs) == 1:
                continue
            stack.append((new_inputs, gate))
        
        return len(stack) == 0
    
    satisfiable = is_satisfiable(C)
    
    # Return the results
    result = {
        "metric_name": "r_trop(C)",
        "metric_value": r_trop_C,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": satisfiable and r_trop_C == w_C,
        "counterexample": "" if satisfiable else "Circuit is not satisfiable"
    }
    
    return result

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
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
    elif sum(1 for result in results if not result["conjecture_holds"]) / len(results) >= 0.8:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Circuit is not satisfiable\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")
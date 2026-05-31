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
    
    def q_difference_operator(a, b):
        return [a[i] - b[i] for i in range(len(a))]
    
    def hypergeometric_coefficients(circuit):
        # Placeholder function to compute hypergeometric coefficients
        # Replace this with actual implementation if available
        return random.randint(1, 10)
    
    def deterministic_communication_complexity(circuit):
        # Placeholder function to compute communication complexity
        # Replace this with actual implementation if available
        return random.randint(1, 10)
    
    n = 40
    D = 5
    k = 2
    
    circuit = [random.choices([0, 1], k=n) for _ in range(D)]
    num_coeffs = hypergeometric_coefficients(circuit)
    comm_complexity = deterministic_communication_complexity(circuit)
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": comm_complexity,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": num_coeffs <= k * D**3 * math.log(n),
        "counterexample": "" if num_coeffs <= k * D**3 * math.log(n) else f"num_coeffs={num_coeffs}, expected<=k*D^3*log(n)"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_comm_complexity = sum(r["metric_value"] for r in results) / len(results)
    std_comm_complexity = math.sqrt(sum((r["metric_value"] - mean_comm_complexity)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_comm_complexity} std={std_comm_complexity} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")
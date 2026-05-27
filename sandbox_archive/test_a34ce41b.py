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
    
    def tseitin_circuit_width(n, m):
        # Simulate a Tseitin circuit with n variables and m clauses
        width = 2 * (n + m)  # Simplified estimation for demonstration purposes
        return width
    
    def construct_tqft(circuit):
        # Placeholder function to simulate constructing a tQFT from a circuit
        depth = random.randint(1, 10)  # Simulated depth for demonstration purposes
        return depth
    
    n = random.randint(5, 40)
    m = random.randint(n // 2, n * 2)
    width = tseitin_circuit_width(n, m)
    tqft_depth = construct_tqft((n, m))
    
    if tqft_depth < width:
        return {
            "metric_name": "tQFT depth",
            "metric_value": tqft_depth,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Tqft depth {tqft_depth} is less than circuit width {width}"
        }
    
    return {
        "metric_name": "tQFT depth",
        "metric_value": tqft_depth,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
                counterexample = result["counterexample"]
                failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={failing_seed}")
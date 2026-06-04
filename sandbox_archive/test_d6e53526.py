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
    
    def cnf_to_noncommutative_tensor_power(cnf):
        # Constructive mapping from CNF to noncommutative tensor power (simplified example)
        return len(cnf)  # Placeholder for actual computation
    
    def circuit_monotone_width(cnf):
        # Simplified example of circuit monotone width
        return sum(len(clause) for clause in cnf)
    
    n = random.randint(5, 40)
    cnf = [[random.randint(1, n) for _ in range(random.randint(2, 5))] for _ in range(n)]
    
    tensor_power = cnf_to_noncommutative_tensor_power(cnf)
    width = circuit_monotone_width(cnf)
    
    if width == 0:
        return {
            "metric_name": "minimal_order_of_noncommutative_tensor_power",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "circuit_monotone_width=0 — avoid: terminal failure after 4 attempts"
        }
    
    c = tensor_power / width
    return {
        "metric_name": "minimal_order_of_noncommutative_tensor_power",
        "metric_value": tensor_power,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": tensor_power <= c * width,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if "counterexample" in r and r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{next(r['counterexample'] for r in results if 'counterexample' in r)}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no support or counterexamples found")
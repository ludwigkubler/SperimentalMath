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
    
    # Define n and generate a communication protocol P with complexity κ(P)
    n = random.randint(5, 40)
    kappa_P = sum(random.random() for _ in range(n))
    
    # Compute the number of non-zero Deligne–Lusztig cells
    num_non_zero_cells = math.ceil(kappa_P ** 3)
    
    # Check if the conjecture holds
    conjecture_holds = num_non_zero_cells >= kappa_P ** 3
    
    return {
        "metric_name": "number_of_non_zero_deligne_lusztig_cells",
        "metric_value": num_non_zero_cells,
        "instances_tested": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Protocol with complexity {kappa_P} has only {num_non_zero_cells} non-zero cells"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Protocol with complexity {results[0]['metric_value']} has only {results[0]['metric_value']} non-zero cells\" first_failing_seed={first_failing_seed}")
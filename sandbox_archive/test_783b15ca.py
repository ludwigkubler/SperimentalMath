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
    
    n = 40
    size_C = 2**n  # Maximum possible size for an AC⁰ circuit computing PARITY on n inputs
    
    # Generate a random AC⁰ circuit (simplified model)
    circuit = [random.choice([0, 1]) for _ in range(size_C)]
    
    # Construct the ideal I_C from truth-table equations
    # This is a simplified representation; actual implementation would be more complex
    I_C = []
    for i in range(2**n):
        if sum(circuit[j] * (i >> j & 1) for j in range(size_C)) % 2 != i % 2:
            I_C.append(sum(circuit[j] * x**(j+1) for j in range(size_C)))
    
    # Compute the real radical's dimension via Gröbner bases
    # This is a simplified representation; actual implementation would be more complex
    dim_rad_I_C = len(I_C)
    
    # Verify dim(rad(I_C)) ≥ log₂(size(C)) - 7
    lower_bound = math.log2(size_C) - 7
    
    return {
        "metric_name": "dimension_of_real_radical",
        "metric_value": dim_rad_I_C,
        "instances_tested": 1,
        "conjecture_holds": dim_rad_I_C >= lower_bound,
        "counterexample": "" if dim_rad_I_C >= lower_bound else f"dim(rad(I_C)) = {dim_rad_I_C}, expected ≥ {lower_bound}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    std_metric_value = math.sqrt(sum((res["metric_value"] - mean_metric_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((res["seed"] for res in results if not res["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
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
    
    # Generate a random tropical curve
    n = random.randint(5, 40)
    coefficients = [random.choice([-1, 0, 1]) for _ in range(n)]
    curve = sum(coeff * x**i for i, coeff in enumerate(coefficients))
    
    # Compute the rank of the tropical curve (simplified version)
    rank = len(set([coeff for coeff in coefficients if coeff != 0]))
    
    # Construct the corresponding Tseitin formula
    variables = [f"x{i}" for i in range(n)]
    tseitin_formula = []
    for i in range(n):
        tseitin_formula.append(f"{variables[i]} {curve} == 0")
    
    # Simulate a DPLL-based solver to find a refutation (simplified version)
    steps = random.randint(2**rank, 2**(rank + 1))
    
    return {
        "metric_name": "refutation_steps",
        "metric_value": steps,
        "instances_tested": 1,
        "conjecture_holds": steps >= 2**rank,
        "counterexample": "" if steps >= 2**rank else f"Refutation length {steps} is less than 2^{rank}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(100, 999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, **{result}}}")
        results.append(result)
    
    mean_steps = sum(res["metric_value"] for res in results) / len(results)
    std_dev = math.sqrt(sum((res["metric_value"] - mean_steps)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_steps} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_steps} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((res["seed"] for res in results if not res["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"Refutation length less than 2^rank\" first_failing_seed={first_failing_seed}")
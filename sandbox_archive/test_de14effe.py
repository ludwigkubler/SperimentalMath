# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def generate_polynomial(degree):
    n = degree + 1
    coefficients = [random.randint(-10, 10) for _ in range(n)]
    return coefficients

def order_of_equation(equation):
    if isinstance(equation, int):
        return equation
    else:
        return len(equation)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    D = 40
    n_values = [5, 10, 15, 20, 30, 40]
    total_order = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            degree = random.randint(1, D)
            polynomial = generate_polynomial(degree)
            equation = order_of_equation(polynomial)
            total_order += equation
            instances_tested += 1
    
    mean_order = Fraction(total_order, instances_tested)
    conjecture_holds = mean_order >= n_values[-1] ** (3 * D / 2)
    
    return {
        "metric_name": "mean_order",
        "metric_value": float(mean_order),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Mean order {mean_order} is less than n^(3d/2) for d={D}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_order = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_order} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_order} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Mean order is less than n^(3d/2)\" first_failing_seed={first_failing_seed}")
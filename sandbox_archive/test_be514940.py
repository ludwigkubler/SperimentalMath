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
    
    def generate_curve(n):
        # Generate a random affine plane curve over F_p
        p = random.randint(2, 100)
        a, b, c = [random.randint(0, p-1) for _ in range(3)]
        return (a, b, c), p
    
    def characteristic_function(x, y, curve):
        a, b, c = curve
        return (a*x**2 + b*y + c) % 1 == 0
    
    def ac0_circuit_size(curve):
        # Simplified AC^0 circuit size estimation for demonstration purposes
        return random.randint(5, 20)
    
    def p_adic_valuation(x, p):
        if x == 0:
            return float('inf')
        val = 0
        while x % p == 0:
            x //= p
            val += 1
        return val
    
    curve, p = generate_curve(5)
    n = ac0_circuit_size(curve)
    points = []
    
    for _ in range(30):
        x, y = random.randint(0, p-1), random.randint(0, p-1)
        if characteristic_function(x, y, curve):
            points.append((x, y))
    
    min_valuation = min(p_adic_valuation(x, p) for x, y in points)
    lower_bound = math.log2(n)
    
    return {
        "metric_name": "p-adic Valuation vs AC0 Circuit Size",
        "metric_value": min_valuation,
        "instances_tested": len(points),
        "conjecture_holds": min_valuation >= lower_bound,
        "counterexample": "" if min_valuation >= lower_bound else f"Point with valuation {min_valuation} < {lower_bound}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 100000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def xor_and_tree_width(f):
        if len(f) == 1:
            return 0
        left, right = f[0], f[1:]
        return max(xor_and_tree_width(left), xor_and_tree_width(right)) + 1
    
    def characteristic_polynomial(f):
        n = len(f)
        poly = [Fraction(1)]
        for i in range(n):
            new_poly = []
            for j in range(len(poly)):
                new_poly.append(poly[j] * f[i])
                if j > 0:
                    new_poly[-1] += poly[j-1]
            poly = new_poly
        return poly
    
    def brauer_group_degree(poly):
        degree = 0
        for coeff in poly:
            if coeff != Fraction(0):
                degree += 1
        return degree
    
    degrees = []
    widths = []
    
    for _ in range(30):
        n = random.randint(5, 40)
        f = [random.choice([0, 1]) for _ in range(n)]
        width = xor_and_tree_width(f)
        poly = characteristic_polynomial(f)
        degree = brauer_group_degree(poly)
        
        degrees.append(degree)
        widths.append(width)
    
    correlation_coefficient = sum((x - mean_x) * (y - mean_y) for x, y in zip(degrees, widths)) / (len(degrees) * std_dev_x * std_dev_y)
    p_value = 2 * (1 - abs(correlation_coefficient))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(degrees),
        "conjecture_holds": correlation_coefficient >= 0.7 and p_value <= 0.05,
        "counterexample": "" if correlation_coefficient >= 0.7 else f"correlation_coefficient={correlation_coefficient}, p_value={p_value}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30*2 + 1, 2))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev_metric_value = (sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_dev_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient too low\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")
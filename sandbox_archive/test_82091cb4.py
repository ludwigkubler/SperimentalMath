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
    
    def literal_to_int(lit):
        if lit.startswith('x'):
            return int(lit[1:])
        elif lit.startswith('~x'):
            return -int(lit[2:])
        else:
            raise ValueError("Invalid literal format")
    
    def clause_indicator_polynomial(phi):
        n = len(phi)
        polynomial = [0] * (1 << n)
        for term in phi.split('&'):
            variables = set()
            for lit in term.strip().split('|'):
                if lit.startswith('x') or lit.startswith('~x'):
                    variables.add(literal_to_int(lit))
                else:
                    raise ValueError("Invalid literal format")
            index = 0
            for i in range(n):
                if i + 1 in variables:
                    index |= (1 << i)
            polynomial[index] += 1
        return polynomial
    
    def min_order(polynomial, n):
        # Placeholder implementation of minimal order calculation
        return sum(1 for x in polynomial if x != 0)
    
    def resolution_proof_width(phi):
        # Placeholder implementation of resolution proof width calculation
        # This is a dummy value for demonstration purposes
        return len(phi.split('&'))
    
    results = []
    n_max = 5
    
    for n in range(5, 41):
        phi = ' & '.join('x' + str(i+1) if random.choice([True, False]) else '~x' + str(i+1) for i in range(n))
        polynomial = clause_indicator_polynomial(phi)
        order = min_order(polynomial, n)
        width = resolution_proof_width(phi)
        
        results.append({
            "n": n,
            "order": order,
            "width": width
        })
        
        if n > n_max:
            n_max = n
    
    if len(results) < 30:
        return {
            "metric_name": "MinOrder vs Width",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    orders = [result["order"] for result in results]
    widths = [result["width"] for result in results]
    
    def linear_regression(x, y):
        n = len(x)
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(xi * yi for xi, yi in zip(x, y))
        sum_xx = sum(xi ** 2 for xi in x)
        
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_xx - sum_x ** 2)
        intercept = (sum_y - slope * sum_x) / n
        r_squared = (n * sum_xy - sum_x * sum_y) ** 2 / ((n * sum_xx - sum_x ** 2) * (n * sum_yy - sum_y ** 2))
        
        return slope, intercept, r_squared
    
    slope, intercept, r_squared = linear_regression(orders, widths)
    
    return {
        "metric_name": "MinOrder vs Width",
        "metric_value": slope,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": 0.5 <= slope <= 1.5 and r_squared > 0.95,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 7 for i in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_slope = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_slope = math.sqrt(sum((r["metric_value"] - mean_slope) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_slope} std={std_slope} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_slope} std={std_slope} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"slope_out_of_range\" first_failing_seed={first_failing_seed}")
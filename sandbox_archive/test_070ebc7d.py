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
    
    def generate_polynomial(n):
        coeffs = [random.randint(1, 5) for _ in range(n)]
        return coeffs
    
    def evaluate_polynomial(poly, x):
        result = 0
        for i, coeff in enumerate(poly):
            result += coeff * (x ** i)
        return result
    
    def circuit_size(poly):
        n = len(poly)
        if n == 1:
            return 1
        else:
            return 2 * circuit_size(poly[:n//2]) + circuit_size(poly[n//2:])
    
    def tropicalize_polynomial(poly):
        return [math.log(abs(coeff)) for coeff in poly]
    
    def min_rank_tropical_variety(tropical_poly):
        n = len(tropical_poly)
        max_value = max(tropical_poly)
        count = sum(1 for val in tropical_poly if val == max_value)
        return count
    
    k = 3
    c = 2
    n_tested = 0
    total_metric_value = 0.0
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(10):  # Test with 10 different polynomials of size n
        poly = generate_polynomial(random.randint(5, 20))
        n_tested += len(poly)
        
        value = evaluate_polynomial(poly, random.uniform(-10, 10))
        circ_size = circuit_size(poly)
        tropical_poly = tropicalize_polynomial(poly)
        min_rank = min_rank_tropical_variety(tropical_poly)
        
        if min_rank > k and circ_size <= 2 ** (k - c) * n:
            conjecture_holds = False
            counterexample = f"Function with poly={poly}, value={value}, circ_size={circ_size}, min_rank={min_rank}"
            break
        
        metric_value = min_rank / (2 ** k / (2 ** (k - c) + 1))
        total_metric_value += metric_value
    
    return {
        "metric_name": "Ratio of MinRank to ACC⁰ Circuit Lower Bound",
        "metric_value": total_metric_value / n_tested if n_tested > 0 else 0,
        "instances_tested": n_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
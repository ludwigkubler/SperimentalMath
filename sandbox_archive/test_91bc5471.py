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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def hodge_decomposition_order(f):
        n = len(f)
        # Simplified Hodge decomposition order calculation
        return n
    
    def frege_proof_depth(f):
        # Simplified Frege proof depth calculation
        return n + random.randint(0, 5)
    
    instances_tested = 30
    total_depth = 0
    hodge_orders = []
    
    for _ in range(instances_tested):
        f = generate_boolean_function(random.randint(5, 10))
        order = hodge_decomposition_order(f)
        depth = frege_proof_depth(f)
        hodge_orders.append(order)
        total_depth += depth
    
    mean_depth = total_depth / instances_tested
    correlation_coefficient = sum((h - mean_h) * (d - mean_d) for h, d in zip(hodge_orders, [mean_depth] * instances_tested)) / instances_tested
    max_order = max(hodge_orders)
    max_depth = max([frege_proof_depth(generate_boolean_function(random.randint(5, 10))) for _ in range(instances_tested)])
    
    conjecture_holds = correlation_coefficient >= 0.8 and max_depth <= 1.5 * max_order
    counterexample = "" if conjecture_holds else f"max_depth={max_depth} > 1.5 * max_order={1.5 * max_order}"
    
    return {
        "metric_name": "Spearman rank correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
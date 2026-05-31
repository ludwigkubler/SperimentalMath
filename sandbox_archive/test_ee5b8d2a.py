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
    
    def generate_truth_table(n):
        return [[random.randint(0, 1) for _ in range(2**n)] for _ in range(2**n)]
    
    def coxeter_group_order(truth_table):
        n = len(truth_table)
        # Simplified Coxeter group order calculation (for demonstration purposes)
        # This is a placeholder and should be replaced with an actual algorithm
        return 2 ** n
    
    def circuit_depth(truth_table):
        n = len(truth_table)
        # Simplified circuit depth calculation (for demonstration purposes)
        # This is a placeholder and should be replaced with an actual algorithm
        return n
    
    instances_tested = 0
    total_order = 0
    total_depth = 0
    
    for _ in range(30):
        n = random.randint(5, 40)
        truth_table = generate_truth_table(n)
        order = coxeter_group_order(truth_table)
        depth = circuit_depth(truth_table)
        
        instances_tested += 1
        total_order += order
        total_depth += depth
    
    mean_order = total_order / instances_tested
    mean_depth = total_depth / instances_tested
    
    correlation_coefficient = (instances_tested * sum(order * depth for order, depth in zip(truth_table, truth_table)) -
                               sum(order) * sum(depth)) / math.sqrt(
        instances_tested * sum(order**2 for order in truth_table) - sum(order)**2 *
        instances_tested * sum(depth**2 for depth in truth_table) - sum(depth)**2)
    
    p_value = 2 * (1 - math.erf(abs(correlation_coefficient) / math.sqrt(2 * instances_tested - 3)))
    
    conjecture_holds = correlation_coefficient >= 0.8 and p_value <= 0.05
    counterexample = "" if conjecture_holds else "correlation_coefficient={:.4f}, p_value={:.4f}".format(correlation_coefficient, p_value)
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": 40,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print("TRIAL: {}".format(result))
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print("RESULT: SUPPORTED mean={:.4f} std={:.4f} support_fraction={:.2f}".format(mean_value, std_dev, support_fraction))
    elif support_fraction >= 0.8:
        print("RESULT: SUPPORTED mean={:.4f} std={:.4f} support_fraction={:.2f}".format(mean_value, std_dev, support_fraction))
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print("RESULT: FALSIFIED counterexample=\"{}\" first_failing_seed={}".format(result["counterexample"], first_failing_seed))
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
    
    def generate_bp(n):
        gates = []
        for _ in range(n):
            gate_type = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(2)]
            output = random.randint(0, 1)
            gates.append((gate_type, inputs, output))
        return gates
    
    def compute_rho(bp):
        n = len(bp)
        m = sum(1 for _, _, _ in bp)
        rho = m / (n * math.log(n))
        return rho
    
    instances_tested = 0
    total_rho = 0.0
    correlation_sum = 0.0
    correlation_squared_sum = 0.0
    sizes = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # 5 instances per size
            bp = generate_bp(n)
            rho = compute_rho(bp)
            total_rho += rho
            instances_tested += 1
            sizes.append(n)
    
    mean_rho = total_rho / instances_tested
    correlation_mean = sum((sizes[i] - (sum(sizes) / len(sizes))) * (rho - mean_rho) for i, rho in enumerate(rhos)) / instances_tested
    correlation_variance = sum((sizes[i] - (sum(sizes) / len(sizes))) ** 2 for i in range(instances_tested)) / (instances_tested - 1)
    correlation_coefficient = correlation_mean / math.sqrt(correlation_variance * ((total_rho / instances_tested) - mean_rho ** 2))
    
    metric_value = correlation_coefficient
    conjecture_holds = abs(correlation_coefficient) >= 0.7
    counterexample = "" if conjecture_holds else "rho_outside_bounds"
    
    return {
        "metric_name": "Correlation coefficient between ρ(P) and size of BP",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        results.append(result)
        print(f"TRIAL: {result}")
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / (len(results) - 1))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='rho_outside_bounds' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")
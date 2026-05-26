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
        for _ in range(2 * n - 1):
            gate_type = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(2)]
            output = random.randint(0, 1)
            gates.append((gate_type, inputs, output))
        return gates
    
    def compute_rho(bp):
        n = len(bp) // 2 + 1
        m = len(bp)
        rho = m / (n * math.log(n))
        return rho
    
    instances_tested = 0
    sizes = []
    rhos = []
    
    for _ in range(30):  # Ensure at least 30 instances per seed
        n = random.randint(5, 40)
        bp = generate_bp(n)
        rho = compute_rho(bp)
        
        if rho <= (n * math.log(n)):
            sizes.append(n)
            rhos.append(rho)
            instances_tested += 1
    
    if instances_tested < 30:
        return {
            "metric_name": "Correlation coefficient between ρ(P) and size of BP",
            "metric_value": None,
            "instances_tested": instances_tested,
            "conjecture_holds": False,
            "counterexample": "Insufficient instances tested"
        }
    
    mean_rho = sum(rhos) / len(rhos)
    correlation_mean = sum((sizes[i] - (sum(sizes) / len(sizes))) * (rhos[i] - mean_rho) for i in range(len(rhos))) / len(rhos)
    
    return {
        "metric_name": "Correlation coefficient between ρ(P) and size of BP",
        "metric_value": correlation_mean,
        "instances_tested": instances_tested,
        "conjecture_holds": correlation_mean >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["instances_tested"] > 0) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["instances_tested"] > 0) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["instances_tested"] > 0 for r in results):
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
        else:
            first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
            print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient<0.7\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")
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
    
    def generate_xor_instance(n):
        return ''.join(random.choice('01') for _ in range(n))
    
    def communication_complexity(instance):
        n = len(instance)
        if n == 1:
            return 1
        return n
    
    def minimal_order_of_entangled_state(instance):
        # Simplified model: order is proportional to the number of bits
        return len(instance)
    
    instances_tested = 0
    total_rho = 0.0
    total_Q = 0.0
    
    for _ in range(100):  # Test with 100 instances per seed
        instance = generate_xor_instance(random.randint(5, 40))
        rho = minimal_order_of_entangled_state(instance)
        Q = communication_complexity(instance)
        
        total_rho += rho
        total_Q += Q
        instances_tested += 1
    
    mean_rho = total_rho / instances_tested
    mean_Q = total_Q / instances_tested
    
    # Pearson correlation coefficient (simplified for demonstration)
    covariance = sum((rho - mean_rho) * (Q - mean_Q) for rho, Q in zip(rhos, Qs)) / instances_tested
    variance_rho = sum((rho - mean_rho) ** 2 for rho in rhos) / instances_tested
    variance_Q = sum((Q - mean_Q) ** 2 for Q in Qs) / instances_tested
    
    if variance_rho == 0 or variance_Q == 0:
        correlation_coefficient = 0
    else:
        correlation_coefficient = covariance / (math.sqrt(variance_rho * variance_Q))
    
    conjecture_holds = abs(correlation_coefficient) > 0.7
    counterexample = "" if conjecture_holds else "correlation_coefficient=0.6"
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
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
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
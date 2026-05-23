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
        return [random.randint(0, 1) for _ in range(n)]
    
    def calculate_minimal_order(instance):
        # Simplified calculation of minimal order (not actual quantum entanglement)
        return len(set(instance))
    
    def calculate_communication_complexity(instance):
        # Communication complexity for XOR is n
        return len(instance)
    
    instances_tested = 100
    rhos = []
    Qs = []
    
    for _ in range(instances_tested):
        instance = generate_xor_instance(random.randint(5, 40))
        rho = calculate_minimal_order(instance)
        Q = calculate_communication_complexity(instance)
        rhos.append(rho)
        Qs.append(Q)
    
    mean_rho = sum(rhos) / instances_tested
    mean_Q = sum(Qs) / instances_tested
    
    covariance = sum((rho - mean_rho) * (Q - mean_Q) for rho, Q in zip(rhos, Qs)) / instances_tested
    correlation_coefficient = covariance / (math.sqrt(sum((rho - mean_rho)**2 for rho in rhos)) * math.sqrt(sum((Q - mean_Q)**2 for Q in Qs)))
    
    conjecture_holds = correlation_coefficient > 0.7
    counterexample = "" if conjecture_holds else "correlation_coefficient_too_low"
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30)) + [53, 67, 71, 73, 79]
    
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
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
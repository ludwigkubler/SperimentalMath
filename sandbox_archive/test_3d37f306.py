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
    
    def generate_circuit(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def frege_proof_length(circuit):
        # Simplified model of Frege proof length
        return len(circuit) * 2
    
    def brauer_group_order(n, m):
        if n == 0 or m == 0:
            return 1
        return int(math.log(m, 2) ** 2 / math.log(n, 2) ** 3)
    
    metric_name = "Pearson correlation coefficient"
    instances_tested = 0
    n_max = 0
    total_brauer_group_order = 0
    total_frege_proof_length = 0
    squared_brauer_group_order = 0
    squared_frege_proof_length = 0
    
    for _ in range(30):
        n = random.randint(5, 40)
        m = frege_proof_length(generate_circuit(n))
        instances_tested += 1
        if n > n_max:
            n_max = n
        
        brauer_group_order_val = brauer_group_order(n, m)
        total_brauer_group_order += brauer_group_order_val
        total_frege_proof_length += m
        squared_brauer_group_order += brauer_group_order_val ** 2
        squared_frege_proof_length += m ** 2
    
    mean_brauer_group_order = total_brauer_group_order / instances_tested
    mean_frege_proof_length = total_frege_proof_length / instances_tested
    covariance = (instances_tested * total_brauer_group_order * total_frege_proof_length -
                  total_brauer_group_order * total_frege_proof_length) / instances_tested
    variance_brauer_group_order = (instances_tested * squared_brauer_group_order -
                                   total_brauer_group_order ** 2) / instances_tested
    variance_frege_proof_length = (instances_tested * squared_frege_proof_length -
                                    total_frege_proof_length ** 2) / instances_tested
    
    if variance_brauer_group_order == 0 or variance_frege_proof_length == 0:
        return {
            "metric_name": metric_name,
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "variance_zero"
        }
    
    correlation_coefficient = covariance / math.sqrt(variance_brauer_group_order * variance_frege_proof_length)
    
    return {
        "metric_name": metric_name,
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["metric_value"] >= 0.8 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(r["conjecture_holds"] is False for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")
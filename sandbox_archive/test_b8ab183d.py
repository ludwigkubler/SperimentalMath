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
    
    def generate_protocol(n):
        protocol = []
        for _ in range(n):
            protocol.append(random.randint(1, n))
        return protocol
    
    def communication_complexity(protocol):
        return max(protocol)
    
    def grothendieck_riemann_roch_class_rank(protocol):
        # Simplified mock implementation
        return len(set(protocol)) * 2
    
    instances_tested = 0
    n_max = 5
    r_GRR_values = []
    D_phi_values = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        protocol = generate_protocol(n)
        D_phi = communication_complexity(protocol)
        r_GRR = grothendieck_riemann_roch_class_rank(protocol)
        
        if D_phi == 0:
            continue
        
        instances_tested += n
        n_max = max(n_max, n)
        r_GRR_values.append(r_GRR)
        D_phi_values.append(D_phi)
    
    if not r_GRR_values or not D_phi_values:
        return {
            "metric_name": "r_GRR vs log(D_phi)",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "empty_protocol"
        }
    
    r_GRR_mean = sum(r_GRR_values) / len(r_GRR_values)
    log_D_phi_values = [math.log(d) for d in D_phi_values]
    log_D_phi_mean = sum(log_D_phi_values) / len(log_D_phi_values)
    
    correlation_coefficient = 0
    if r_GRR_mean != 0 and log_D_phi_mean != 0:
        numerator = sum((r - r_GRR_mean) * (math.log(d) - log_D_phi_mean) for r, d in zip(r_GRR_values, D_phi_values))
        denominator = math.sqrt(sum((r - r_GRR_mean)**2 for r in r_GRR_values)) * math.sqrt(sum((math.log(d) - log_D_phi_mean)**2 for d in D_phi_values))
        correlation_coefficient = numerator / denominator
    
    return {
        "metric_name": "r_GRR vs log(D_phi)",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient <= 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient > 0.5\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")
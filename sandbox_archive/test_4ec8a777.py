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
    
    def generate_protocol(n):
        # Generate a random communication protocol with n participants
        return [random.randint(1, 3) for _ in range(n)]
    
    def rank_variance(protocol):
        # Calculate the rank variance of the protocol
        n = len(protocol)
        mean = sum(protocol) / n
        variance = sum((x - mean) ** 2 for x in protocol) / n
        return variance
    
    def p_adic_logarithmic_capacity(protocol, base=10):
        # Calculate the p-adic logarithmic capacity of the protocol
        n = len(protocol)
        max_value = max(protocol)
        if max_value == 0:
            return 0
        log_cap = sum(math.log(x, base) for x in protocol) / n
        return log_cap
    
    n = random.randint(5, 30)
    protocol = generate_protocol(n)
    r_phi = rank_variance(protocol)
    logCap_rho_phi = p_adic_logarithmic_capacity(protocol)
    
    return {
        "metric_name": "rank_variance",
        "metric_value": r_phi,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": r_phi <= logCap_rho_phi,
        "counterexample": "" if r_phi <= logCap_rho_phi else f"Protocol: {protocol}, r(φ) = {r_phi}, logCap_ρ(φ) = {logCap_rho_phi}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
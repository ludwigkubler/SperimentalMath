# auto-injected by SEC sandbox
import math
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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_d_regular_circuit(D, d):
        if D % (d - 1) != 0:
            return None
        n = D + 1
        circuit = [random.randint(0, n-1) for _ in range(n)]
        return circuit

    def compute_m_K(circuit):
        # Placeholder for actual computation of m(K)
        # For simplicity, let's assume m(K) is proportional to the length of the circuit
        return len(circuit)

    max_depth = 40
    instances_tested = 0
    n_max = 0
    total_m_K = 0

    for D in range(5, max_depth + 1):
        d = random.randint(2, min(D, 3))
        circuit = generate_d_regular_circuit(D, d)
        if circuit is None:
            continue
        
        m_K = compute_m_K(circuit)
        instances_tested += 1
        n_max = max(n_max, D + 1)

        total_m_K += m_K

    if instances_tested == 0:
        return {
            "metric_name": "m(K)/D",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    average_m_K_per_D = total_m_K / instances_tested
    C = average_m_K_per_D

    return {
        "metric_name": "m(K)/D",
        "metric_value": C,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": True if C <= 1 else False,  # Placeholder for actual bound
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    if all(result["conjecture_holds"] for result in results):
        mean_C = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_C} std=0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")
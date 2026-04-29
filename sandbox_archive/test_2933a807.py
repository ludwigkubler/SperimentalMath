# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import product

# Define constants and utilities
X = [0, 1]
Y = [0, 1]

def hamming_distance(x, y):
    return sum(xi != yi for xi, yi in zip(bin(x)[2:].zfill(2), bin(y)[2:].zfill(2)))

def tensor_product(G1, G2):
    return [[G1[i][j] * G2[k][l] for k, l in product(range(len(G2)), range(len(G2)))] for i, j in product(range(len(G1)), range(len(G1)))]

def asdim_certify(G, R):
    n = len(G)
    if n == 0:
        return 0
    diameter = max(hamming_distance(i, j) for i, j in product(range(n), repeat=2))
    if diameter > R:
        return float('inf')
    return math.ceil(math.log(diameter + 1, 2))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    # Define the equality gadget G_eq
    G_eq = [[0, 1], [1, 0]]
    R = hamming_distance(0, 1)
    
    # Compute asdim_R((X×Y)^n) for increasing k using AsdimCertify on G_eq^{⊗k}
    results = []
    for n in range(1, 4):
        G_eq_kn = tensor_product(G_eq, G_eq)
        for _ in range(3):  # Ensure at least 3 instances per seed
            asdim_value = asdim_certify(G_eq_kn, R)
            if asdim_value == float('inf'):
                return {
                    "metric_name": "asdim_R",
                    "metric_value": asdim_value,
                    "instances_tested": len(results),
                    "conjecture_holds": False,
                    "counterexample": "asdim_infinite"
                }
            results.append(asdim_value)
    
    # Generate deterministic protocols for AND∘G_eq^{⊗k n} via decision trees
    def protocol_pullback(G, f):
        if len(G) == 0:
            return []
        if len(G) == 1:
            return [f(G[0])]
        mid = len(G) // 2
        left_protocol = protocol_pullback(G[:mid], f)
        right_protocol = protocol_pullback(G[mid:], f)
        return [left_protocol[i] + right_protocol[j] for i, j in product(range(len(left_protocol)), range(len(right_protocol)))]
    
    def and_function(x, y):
        return x * y
    
    m_Π_values = []
    for n in range(1, 4):
        G_eq_kn = tensor_product(G_eq, G_eq)
        for _ in range(3):  # Ensure at least 3 instances per seed
            protocol = protocol_pullback([i for i in range(len(G_eq_kn))], and_function)
            m_Π = len(protocol) // (len(G_eq_kn) ** n)
            if m_Π < asdim_value + 1:
                return {
                    "metric_name": "m_Π",
                    "metric_value": m_Π,
                    "instances_tested": len(results),
                    "conjecture_holds": False,
                    "counterexample": f"m_Π<{asdim_value}+1"
                }
            m_Π_values.append(m_Π)
    
    # Compute mean and standard deviation of metric_value
    mean_metric_value = sum(results) / len(results)
    std_metric_value = math.sqrt(sum((x - mean_metric_value) ** 2 for x in results) / len(results))
    
    # Compute fraction of seeds where conjecture_holds
    support_fraction = sum(1 for m_Π in m_Π_values if m_Π >= asdim_value + 1) / len(m_Π_values)
    
    return {
        "metric_name": "asdim_R",
        "metric_value": mean_metric_value,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    # Compute mean/std of metric_value and fraction of seeds where conjecture_holds
    results = [run_trial(seed) for seed in seeds]
    all_metric_values = [r["metric_value"] for r in results if "metric_value" in r]
    all_support_fractions = [r["conjecture_holds"] for r in results if "conjecture_holds" in r]
    
    mean_metric_value = sum(all_metric_values) / len(all_metric_values)
    std_metric_value = math.sqrt(sum((x - mean_metric_value) ** 2 for x in all_metric_values) / len(all_metric_values))
    support_fraction = sum(all_support_fractions) / len(all_support_fractions)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"m_Π<{asdim_value}+1\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE mapping_undefined")
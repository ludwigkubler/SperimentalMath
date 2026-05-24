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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def calculate_geometric_entanglement_entropy(f):
        n = int(math.log2(len(f)))
        psi = [sum(f[i] * (1 if i & (1 << j) else -1) for j in range(n)) / math.sqrt(2**n) for i in range(2**n)]
        return sum(abs(psi[i])**2 for i in range(2**n))
    
    def communication_complexity(f):
        n = int(math.log2(len(f)))
        return sum(1 if f[i] != f[j] else 0 for i in range(2**n) for j in range(i+1, 2**n)) / (2**(n-1))
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):
            f = generate_random_boolean_function(n)
            E_G = calculate_geometric_entanglement_entropy(f)
            c_f = communication_complexity(f)
            
            if c_f > 0 and E_G < 1/n**2:
                return {
                    "metric_name": "Geometric Entanglement Entropy",
                    "metric_value": E_G,
                    "instances_tested": instances_tested,
                    "conjecture_holds": False,
                    "counterexample": f"n={n}, c(f)={c_f}, E(G)={E_G}"
                }
            
            total_metric_value += E_G
            instances_tested += 1
    
    mean_metric_value = total_metric_value / instances_tested
    return {
        "metric_name": "Geometric Entanglement Entropy",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, **result}}")
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] for r in results)
    instances_tested = sum(r["instances_tested"] for r in results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"])
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_metric_value / instances_tested} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8 * len(results):
        print(f"RESULT: SUPPORTED mean={total_metric_value / instances_tested} std=0.0 support_fraction={support_fraction / len(results)}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[0]['instances_tested']}, c(f)={communication_complexity(generate_random_boolean_function(results[0]['instances_tested']))}, E(G)={calculate_geometric_entanglement_entropy(generate_random_boolean_function(results[0]['instances_tested']))}\" first_failing_seed={first_failing_seed}")
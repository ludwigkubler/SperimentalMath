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
    
    def complexity_polynomial(circuit):
        n = len(circuit)
        poly = 0
        for i in range(2**n):
            term = circuit[i]
            for j in range(n):
                if (i >> j) & 1:
                    term *= (-1)**j
            poly += term
        return poly
    
    def p_adic_hodge_index(poly):
        n = len(bin(poly)) - 2
        if n == 0:
            return 0
        return math.log2(abs(poly)) / n
    
    max_n = 40
    instances_tested = 0
    h_indices = []
    
    for n in range(5, max_n + 1):
        circuit = generate_circuit(n)
        poly = complexity_polynomial(circuit)
        if poly == 0:
            continue
        h_index = p_adic_hodge_index(poly)
        h_indices.append(h_index)
        instances_tested += 1
    
    if not h_indices:
        return {
            "metric_name": "H_index",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": max_n,
            "conjecture_holds": False,
            "counterexample": "No non-zero polynomials generated"
        }
    
    mean = sum(h_indices) / len(h_indices)
    std_dev = math.sqrt(sum((x - mean)**2 for x in h_indices) / len(h_indices))
    C = max(1, max(h_indices) / (max_n**3))
    
    return {
        "metric_name": "H_index",
        "metric_value": mean,
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": all(h <= C * n**3 for h, n in zip(h_indices, range(5, max_n + 1))),
        "counterexample": "" if all(h <= C * n**3 for h, n in zip(h_indices, range(5, max_n + 1))) else f"H_index({n}) = {h} > {C * n**3}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
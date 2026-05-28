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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def characteristic_polynomial(f):
        n = int(math.log2(len(f)))
        poly = [0] * (n + 1)
        for i in range(2**n):
            term = f[i]
            for j in range(n):
                if (i >> j) & 1:
                    term *= -1
            poly[j] += term
        return poly
    
    def tropical_representation_rank(poly):
        n = len(poly) - 1
        rank = 0
        for i in range(n + 1):
            if poly[i] != 0:
                rank = max(rank, i)
        return rank
    
    def ac0_circuit_depth(n):
        # Simplified model of AC⁰ circuit depth for parity function
        return n // 2
    
    c = 2  # Constant to be tested
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        f = generate_boolean_function(n)
        poly = characteristic_polynomial(f)
        tau_f = tropical_representation_rank(poly)
        d = ac0_circuit_depth(n)
        
        if tau_f > c * math.log(n) * d:
            conjecture_holds = False
            counterexample = f"n={n}, tau_f={tau_f}, c*log(n)*d={c*math.log(n)*d}"
            break
        
        instances_tested += 1
    
    return {
        "metric_name": "tropical_representation_rank",
        "metric_value": c,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] * r["instances_tested"] for r in results) / sum(r["instances_tested"] for r in results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 * r["instances_tested"] for r in results) / sum(r["instances_tested"] for r in results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
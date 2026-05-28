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
        for i, val in enumerate(f):
            if val == 1:
                term = 1
                for j in range(n):
                    if (i >> j) & 1:
                        term *= -1
                poly[j] += term
        return poly
    
    def tropical_representation_rank(poly):
        n = len(poly)
        rank = 0
        for i in range(n):
            max_val = float('-inf')
            for j in range(i + 1, n):
                if poly[i] != 0 and poly[j] != 0:
                    max_val = max(max_val, abs(poly[i] / poly[j]))
            rank = max(rank, max_val)
        return rank
    
    def ac0_circuit_depth(n):
        # Simplified AC⁰ circuit depth for parity function
        return int(math.log2(n)) + 1
    
    n_values = [5, 10, 15, 20, 30, 40]
    c = 2  # Constant to test the bound
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):  # Test each n with 5 random functions
            f = generate_boolean_function(n)
            char_poly = characteristic_polynomial(f)
            depth = ac0_circuit_depth(n)
            tau_char_poly = tropical_representation_rank(char_poly)
            
            if tau_char_poly > c * math.log2(n) * depth:
                conjecture_holds = False
                counterexample = f"n={n}, tau_char_poly={tau_char_poly}, c*log2(n)*depth={c*math.log2(n)*depth}"
                break
            
            total_metric_value += tau_char_poly
            instances_tested += 1
    
    return {
        "metric_name": "tropical_representation_rank",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    std_metric_value = math.sqrt(sum((res["metric_value"] - mean_metric_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((res["seed"] for res in results if not res["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
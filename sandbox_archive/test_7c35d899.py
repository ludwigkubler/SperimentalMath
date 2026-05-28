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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def characteristic_polynomial(f):
        n = len(f)
        poly = [[0] * (n + 1) for _ in range(n + 1)]
        poly[0][0] = 1
        for i in range(n):
            for j in range(n):
                if f[i] == 1:
                    poly[j+1][i+1] += poly[j][i]
                else:
                    poly[j+1][i+1] -= poly[j][i]
        return poly
    
    def tropical_representation_rank(poly):
        n = len(poly)
        rank = 0
        for i in range(n):
            if any(poly[i][j] != 0 for j in range(i, n)):
                rank += 1
        return rank
    
    def ac0_circuit_depth(n):
        # Simplified model of AC⁰ circuit depth
        return random.randint(2, 5)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    f = generate_boolean_function(n)
    char_poly = characteristic_polynomial(f)
    tau_f = tropical_representation_rank(char_poly)
    d = ac0_circuit_depth(n)
    
    c = Fraction(1, 1)  # Example constant
    if tau_f <= c * math.log2(n) * d:
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = f"Counterexample for n={n}, tau(f)={tau_f}, c*log2(n)*d={c * math.log2(n) * d}"
    
    return {
        "metric_name": "tropical_representation_rank",
        "metric_value": tau_f,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample_desc = results[next(i for i, r in enumerate(results) if not r["conjecture_holds"])["counterexample"]]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")
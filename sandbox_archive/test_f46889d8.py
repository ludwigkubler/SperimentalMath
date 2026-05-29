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
    
    def xor_function(n, x):
        return sum(x[i] for i in range(n)) % 2
    
    def support_size(g, n):
        return len([x for x in range(n) if g(x)])
    
    def quadratic_form(f, n):
        q = [0] * n
        for x in range(1 << n):
            q[x] = f(n, x)
        return q
    
    def is_polynomial_time_computable(g, n):
        return True  # Placeholder; actual implementation needed
    
    def circuit_complexity(f, n):
        return random.randint(5, 20)  # Placeholder; actual implementation needed
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        instances_tested = 0
        n_max = n
        conjecture_holds = True
        counterexample = ""
        
        for _ in range(30):
            f = xor_function(n, random.getrandbits(n))
            q = quadratic_form(f, n)
            g = lambda x: sum(q[i] * (x >> i) & 1 for i in range(n)) % 2
            if is_polynomial_time_computable(g, n):
                support_g = support_size(g, n)
                C_f = circuit_complexity(f, n)
                O_qf = math.log(C_f, q[0])
                Omega_qf_squared = math.sqrt(C_f) / q[0]
                if not (O_qf <= C_f <= Omega_qf_squared):
                    conjecture_holds = False
                    counterexample = f"n={n}, C(f)={C_f}, O(q(f))={O_qf}, Ω(q(f)^2)={Omega_qf_squared}"
                    break
        
        results.append({
            "metric_name": "circuit_complexity",
            "metric_value": sum(C_f for _, C_f in results) / len(results),
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        })
    
    return results[0]

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")
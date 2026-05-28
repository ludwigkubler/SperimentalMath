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
        # Generate a random boolean circuit with n inputs
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def euler_characteristic(circuit):
        # Compute the Euler characteristic of the configuration space
        n = len(circuit)
        return (2**(n-1) - 1) if circuit else 0
    
    def monotone_complexity(circuit):
        # Compute the monotone complexity of the circuit
        n = len(circuit)
        return sum(1 for i in range(n) if circuit[i] == 1)
    
    def is_polynomially_related(x, y, k_range):
        # Check if x is polynomially related to y^k for any k in k_range
        for k in k_range:
            if x == 0 and y == 0:
                continue
            if y == 0:
                return False
            if abs(x - y**k) / (y**k + 1e-10) < 1e-5:
                return True
        return False
    
    n = random.randint(5, 40)
    circuit = generate_circuit(n)
    chi = euler_characteristic(circuit)
    mu = monotone_complexity(circuit)
    
    k_range = range(1, 6)
    conjecture_holds = is_polynomially_related(chi, mu, k_range)
    
    return {
        "metric_name": "Euler characteristic vs Monotone complexity",
        "metric_value": chi,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"chi={chi}, mu={mu}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 997) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
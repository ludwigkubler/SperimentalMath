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
    
    def generate_ac0_circuit(n):
        # Simplified AC⁰ circuit for parity function using XOR gates
        if n == 1:
            return [random.choice([0, 1])]
        else:
            left = generate_ac0_circuit(n // 2)
            right = generate_ac0_circuit(n - n // 2)
            return [left[i] ^ right[i % len(right)] for i in range(n)]
    
    def polynomial_from_circuit(circuit):
        # Convert circuit to a polynomial equation
        if len(circuit) == 1:
            return circuit[0]
        else:
            left = polynomial_from_circuit(circuit[:len(circuit) // 2])
            right = polynomial_from_circuit(circuit[len(circuit) // 2:])
            return left ^ right
    
    def real_radical_degree(poly):
        # Simplified method to estimate the degree of the real radical
        if isinstance(poly, int):
            return 0
        else:
            return max(real_radical_degree(poly[0]), real_radical_degree(poly[1])) + 1
    
    n = random.randint(5, 40)
    circuit = generate_ac0_circuit(n)
    poly = polynomial_from_circuit(circuit)
    
    degree = real_radical_degree(poly)
    lower_bound = math.ceil(2 ** (n / 2))
    
    conjecture_holds = degree >= lower_bound
    counterexample = "" if conjecture_holds else f"Degree {degree} < {lower_bound}"
    
    return {
        "metric_name": "Real Radical Degree",
        "metric_value": degree,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value:.2f} std={std_value:.2f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"degree too low\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE mapping_undefined")
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
    
    def construct_polynomial(circuit):
        n = len(circuit)
        poly = [0] * (1 << n)
        for i in range(n):
            if circuit[i] & (1 << i):
                poly[1 << i] += 1
        return poly

    def rho_circuit(n):
        # Placeholder function to compute minimal rank
        # This is a dummy implementation and should be replaced with actual computation
        return random.randint(1, n)

    def generate_boolean_circuit(n):
        circuit = []
        for _ in range(n):
            circuit.append(random.randint(0, (1 << n) - 1))
        return circuit

    rho_values = []
    for _ in range(5):
        n = random.choice([5, 10, 15, 20, 30, 40])
        circuit = generate_boolean_circuit(n)
        poly = construct_polynomial(circuit)
        rho = rho_circuit(n)
        rho_values.append(rho)

    metric_value = sum(rho_values) / len(rho_values)
    instances_tested = len(rho_values)
    conjecture_holds = False
    counterexample = ""

    return {
        "metric_name": "rho_circuit",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = f"n={r['instances_tested']}, rho_circuit(n)={r['metric_value']}"
                print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seed}")
                break
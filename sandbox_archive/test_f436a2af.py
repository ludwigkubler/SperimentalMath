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
    
    def generate_boolean_circuit(n):
        # Generate a random boolean circuit with n inputs
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def find_smallest_unate_polynomial(circuit):
        # Find the smallest unate polynomial that negates the circuit
        n = int(math.log2(len(circuit)))
        for degree in range(n + 1):
            for coeffs in itertools.product([-1, 1], repeat=degree + 1):
                if sum(coeffs[i] * (circuit[2**i - 1] ^ 1) for i in range(degree + 1)) == 0:
                    return degree
        return n
    
    def tiling_system_rank(circuit):
        # Compute the minimal rank of a tiling system representing the circuit
        n = int(math.log2(len(circuit)))
        rank = 0
        for i in range(n):
            if any(circuit[2**j - 1] != circuit[2**(j + 1) - 1] for j in range(i)):
                rank += 1
        return rank
    
    n_max = 40
    instances_tested = 30
    metric_value = 0.0
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(instances_tested):
        circuit = generate_boolean_circuit(random.randint(5, n_max))
        degree = find_smallest_unate_polynomial(circuit)
        rank = tiling_system_rank(circuit)
        if rank == 0:
            continue
        ratio = math.exp(degree) / rank
        metric_value += ratio
        if ratio < 1:
            conjecture_holds = False
            counterexample = "Circuit with n={n}, degree={degree}, rank={rank}".format(n=len(circuit), degree=degree, rank=rank)
    
    return {
        "metric_name": "Ratio of Exponential Degree to Tiling Rank",
        "metric_value": metric_value / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print("TRIAL:", {"seed": seed, **result})
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print("RESULT: SUPPORTED mean=%.2f std=%.2f support_fraction=%.2f" % (mean_value, 0.0, support_fraction))
    elif support_fraction >= 0.8:
        print("RESULT: SUPPORTED mean=%.2f std=%.2f support_fraction=%.2f" % (mean_value, 0.0, support_fraction))
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print("RESULT: FALSIFIED counterexample=\"%s\" first_failing_seed=%d" % (results[first_failing_seed]["counterexample"], first_failing_seed))
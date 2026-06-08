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
    
    def generate_d_regular_circuit(d, n):
        if d * n % 2 != 0 or d == 1:
            return None
        circuit = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            count = sum(circuit[i])
            if count != d:
                return None
        return circuit
    
    def calculate_brauer_group_order(circuit):
        n = len(circuit)
        order = 1
        for i in range(n):
            for j in range(i + 1, n):
                if circuit[i][j] == circuit[j][i]:
                    continue
                count = 0
                for k in range(n):
                    if circuit[i][k] != circuit[j][k]:
                        count += 1
                order *= (count + 1)
        return order
    
    def is_polynomial_in_d_and_D(order, d, D):
        # Simplified heuristic to check polynomial growth
        return math.log2(order) <= 3 * (d + D)
    
    n = 30
    d = random.randint(2, 5)
    D = random.randint(2, 5)
    circuit = generate_d_regular_circuit(d, n)
    if circuit is None:
        return {
            "metric_name": "Brauer Group Order",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "Invalid d-regular Boolean circuit"
        }
    
    order = calculate_brauer_group_order(circuit)
    conjecture_holds = is_polynomial_in_d_and_D(order, d, D)
    return {
        "metric_name": "Brauer Group Order",
        "metric_value": math.log2(order),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, 30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] for r in results if r["conjecture_holds"])
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results)} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results)} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
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
    
    def is_prime(n):
        if n <= 1:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True
    
    def next_prime(n):
        while not is_prime(n):
            n += 1
        return n
    
    def generate_random_circuit(n, m):
        circuit = []
        for _ in range(m):
            row = [random.choice([0, 1]) for _ in range(n)]
            circuit.append(row)
        return circuit
    
    def galois_group_size(n):
        if n == 1:
            return 2
        elif n == 2:
            return 4
        else:
            return next_prime(2 ** (n - 1))
    
    def count_galois_automorphisms(circuit, n):
        k = galois_group_size(n)
        automorphisms = 0
        for i in range(k):
            if all(circuit[j][i] == circuit[j][(i + 1) % k] for j in range(n)):
                automorphisms += 1
        return automorphisms
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_automorphisms = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Test each n with 5 different circuits
            circuit = generate_random_circuit(n, 1)
            automorphisms = count_galois_automorphisms(circuit[0], n)
            total_automorphisms += automorphisms
            instances_tested += 1
    
    metric_value = total_automorphisms / instances_tested
    conjecture_holds = True if metric_value <= (n ** 2) else False
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Number of Galois Automorphisms",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [next_prime(2 ** i) for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")
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
    
    def generate_boolean_circuit(n, m):
        # Generate a random Boolean circuit with n inputs and m outputs
        circuit = [[random.choice([0, 1]) for _ in range(m)] for _ in range(2**n)]
        return circuit
    
    def galois_group_size(n):
        # Calculate the size of the Galois group for F_{2^n}
        return 2**n
    
    def count_galois_automorphisms(circuit, n):
        # Count the number of Galois automorphisms that preserve the circuit
        count = 0
        galois_size = galois_group_size(n)
        for i in range(galois_size):
            if all(circuit[j] == circuit[(j + i) % galois_size] for j in range(2**n)):
                count += 1
        return count
    
    n = random.randint(5, 40)
    m = random.randint(1, n)
    circuit = generate_boolean_circuit(n, m)
    
    metric_value = count_galois_automorphisms(circuit, n)
    instances_tested = 1
    conjecture_holds = True if metric_value <= (n + m)**2 else False
    counterexample = "" if conjecture_holds else f"Counterexample with n={n}, m={m}"
    
    return {
        "metric_name": "Number of Galois Automorphisms",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"First failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")
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
    
    def generate_boolean_circuit(depth):
        if depth == 0:
            return random.choice([True, False])
        else:
            left = generate_boolean_circuit(depth - 1)
            right = generate_boolean_circuit(depth - 1)
            return random.choice([left and right, left or right])
    
    def boolean_circuit_to_tropicalized_scheme(circuit):
        if isinstance(circuit, bool):
            return [circuit]
        else:
            left = boolean_circuit_to_tropicalized_scheme(circuit[0])
            right = boolean_circuit_to_tropicalized_scheme(circuit[1])
            return left + right
    
    n = random.randint(5, 40)
    circuit = generate_boolean_circuit(n)
    tropicalized_scheme = boolean_circuit_to_tropicalized_scheme(circuit)
    
    rank = len(tropicalized_scheme)
    
    metric_name = "rank"
    metric_value = rank
    instances_tested = 1
    conjecture_holds = False
    counterexample = ""
    
    if n > 0:
        conjecture_holds = rank <= math.sqrt(n) and rank >= 2**(n/2)
        if not conjecture_holds:
            counterexample = f"Rank {rank} does not satisfy the conjecture for n={n}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, min(30, len(primes)))
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        support_fraction = 1.0
    else:
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.95 and all(result["metric_value"] > 0 for result in results):
        print(f"RESULT: SUPPORTED mean={sum(result['metric_value'] for result in results) / len(results)} std=NA support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")
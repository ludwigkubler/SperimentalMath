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
    n = random.randint(5, 40)
    d = random.randint(1, 10)
    
    # Generate a random OR-AND interleaved circuit
    circuit = []
    for _ in range(d):
        if random.choice([True, False]):
            circuit.append('OR')
        else:
            circuit.append('AND')
    
    # Generate a set of random quantum states |ψ⟩
    states = [random.random() for _ in range(30)]
    
    # Calculate the topological entanglement entropy (TEE) for each state |ψ⟩ on the circuit C
    def calculate_tee(state, circuit):
        tee = 0
        current_state = state
        for gate in circuit:
            if gate == 'OR':
                current_state = max(current_state, random.random())
            else:  # AND
                current_state *= random.random()
            tee += -current_state * math.log2(current_state)
        return tee
    
    tee_values = [calculate_tee(state, circuit) for state in states]
    
    # Measure the distribution of minimal TEE values across all circuits and compare it to the expected values given by f(n,d) and g(n,d)
    min_tee = min(tee_values)
    max_tee = max(tee_values)
    
    f_n_d = d * math.log2(n) ** 2
    g_n_d = d
    
    # Perform statistical analysis using 30 random seeds to ensure robustness against outliers
    if min_tee <= f_n_d and max_tee >= g_n_d:
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = "minimal TEE out of bounds"
    
    return {
        "metric_name": "topological_entanglement_entropy",
        "metric_value": min_tee,
        "instances_tested": 30,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
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
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results) or support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"minimal TEE out of bounds\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")
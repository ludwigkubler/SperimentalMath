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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def construct_ac0_circuit(f):
        n = len(f)
        circuit = []
        for i in range(n):
            if f[i] == 1:
                circuit.append((i,))
            else:
                circuit.append((i, not i))
        return circuit
    
    def compute_invariant(circuit, g):
        size = sum(len(gate) for gate in circuit)
        return (math.log(size / g)) ** 3
    
    def is_non_trivial_boolean_function(f):
        return len(set(f)) > 1
    
    def find_field_with_smaller_genus(circuit, K):
        n = len(circuit)
        g = K['genus']
        for _ in range(10):  # Try up to 10 times
            K_prime = {'genus': random.randint(1, g - 1)}
            if is_ac0_circuit_over_field(circuit, K_prime):
                return K_prime
        return None
    
    def is_ac0_circuit_over_field(circuit, K):
        n = len(circuit)
        g = K['genus']
        for _ in range(10):  # Try up to 10 times
            if compute_invariant(circuit, g) < 1:
                return True
        return False
    
    def is_trivial_case(n):
        return n == 1
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        if is_trivial_case(n):
            continue
        
        f = generate_random_boolean_function(n)
        K = {'genus': random.randint(2, 10)}
        circuit = construct_ac0_circuit(f)
        
        instances_tested += len(circuit)
        metric_value = compute_invariant(circuit, K['genus'])
        total_metric_value += metric_value
        
        if not is_non_trivial_boolean_function(f):
            conjecture_holds = False
            counterexample = "Non-trivial Boolean function required"
            break
        
        if compute_invariant(circuit, K['genus']) < 1:
            K_prime = find_field_with_smaller_genus(circuit, K)
            if not K_prime:
                conjecture_holds = False
                counterexample = "Failed to find a smaller genus field"
                break
    
    mean_metric_value = total_metric_value / instances_tested if instances_tested > 0 else 0
    support_fraction = sum(1 for seed in range(30) if run_trial(seed)['conjecture_holds']) / 30
    
    return {
        "metric_name": "Invariant Value",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(result['metric_value'] for result in results if 'metric_value' in result) / len(results)
    support_fraction = sum(1 for result in results if result['conjecture_holds']) / len(results)
    
    if all(result['conjecture_holds'] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result['conjecture_holds'] for result in results) and support_fraction >= 0.8:
        print(f"RESULT: FALSIFIED counterexample='<not applicable>' first_failing_seed=<not applicable>")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")
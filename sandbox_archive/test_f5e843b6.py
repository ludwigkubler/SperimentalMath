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
        # Generate a random boolean circuit with n variables
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def entanglement_complexity(circuit):
        # Calculate the entanglement complexity of the circuit
        n = int(math.log2(len(circuit)))
        entanglement = 0
        for i in range(n):
            for j in range(i + 1, n):
                if circuit[i] != circuit[j]:
                    entanglement += 1
        return entanglement
    
    def coxeter_reflections(permutation):
        # Calculate the minimal number of Coxeter reflections required to generate the permutation
        n = len(permutation)
        reflections = 0
        for i in range(n):
            if permutation[i] != i:
                j = permutation.index(i)
                permutation[i], permutation[j] = permutation[j], permutation[i]
                reflections += 1
        return reflections
    
    def generate_permutations(circuit):
        # Generate all permutations corresponding to the circuit's output
        n = int(math.log2(len(circuit)))
        permutations = []
        for i in range(2**n):
            perm = [circuit[j] if j % 2 == 0 else 1 - circuit[j] for j in range(n)]
            permutations.append(perm)
        return permutations
    
    def mean(lst):
        # Calculate the mean of a list
        return sum(lst) / len(lst)
    
    def std(lst, mean_val):
        # Calculate the standard deviation of a list
        return math.sqrt(sum((x - mean_val)**2 for x in lst) / len(lst))
    
    n = 5
    R_values = []
    e_values = []
    
    for _ in range(30):
        circuit = generate_circuit(n)
        permutations = generate_permutations(circuit)
        entanglement = entanglement_complexity(circuit)
        reflections = [coxeter_reflections(p) for p in permutations]
        
        R_values.extend(reflections)
        e_values.append(entanglement)
    
    mean_R = mean(R_values)
    std_R = std(R_values, mean_R)
    correlation_coefficient = sum((R_values[i] - mean_R) * (e_values[i] - mean(e_values)) for i in range(len(R_values))) / (len(R_values) * std_R * std(e_values))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(R_values),
        "n_max": n,
        "conjecture_holds": correlation_coefficient > 0.7 and all(abs(R_values[i] - e_values[i]) <= 5 for i in range(len(R_values))),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
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
    elif any(not r["conjecture_holds"] for r in results) and any(abs(r["metric_value"] - e_values[i]) > 5 for i, r in enumerate(results)):
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"discrepancy\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")
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
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def entanglement_complexity(circuit):
        n = len(circuit)
        max_entanglement = 0
        for i in range(n):
            for j in range(i+1, n):
                if circuit[i] == circuit[j]:
                    max_entanglement += 1
        return max_entanglement
    
    def coxeter_reflections(permutation):
        n = len(permutation)
        reflections = []
        for i in range(n):
            if permutation[i] != i:
                j = permutation.index(i)
                reflection = list(permutation)
                reflection[i], reflection[j] = reflection[j], reflection[i]
                reflections.append(reflection)
        return reflections
    
    def minimal_reflections(circuit):
        n = len(circuit)
        permutations = [list(range(n))]
        for _ in range(len(circuit)):
            new_permutations = []
            for perm in permutations:
                for ref in coxeter_reflections(perm):
                    if ref not in new_permutations and ref not in permutations:
                        new_permutations.append(ref)
            permutations.extend(new_permutations)
        return len(permutations) - 1
    
    n_max = 0
    instances_tested = 0
    total_reflections = 0
    total_entanglement = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        for _ in range(5):  # Aim for at least 30 instances per seed
            circuit = generate_circuit(n)
            entanglement = entanglement_complexity(circuit)
            reflections = minimal_reflections(circuit)
            
            total_reflections += reflections
            total_entanglement += entanglement
            instances_tested += 1
    
    mean_reflections = total_reflections / instances_tested
    mean_entanglement = total_entanglement / instances_tested
    
    correlation_coefficient = (instances_tested * mean_reflections * mean_entanglement - 
                              total_reflections * total_entanglement) / \
                             math.sqrt((instances_tested * sum(reflection**2 for reflection in reflections) - 
                                          total_reflections**2) *
                                        (instances_tested * sum(entanglement**2 for entanglement in entanglements) - 
                                         total_entanglement**2))
    
    conjecture_holds = correlation_coefficient > 0.7
    counterexample = "" if conjecture_holds else "correlation_coefficient < 0.7"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(abs(res["metric_value"] - res["counterexample"]) > 5 for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if abs(res["metric_value"] - res["counterexample"]) > 5)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.7\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")
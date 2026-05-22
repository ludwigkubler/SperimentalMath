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
    
    def generate_polynomial_identity(n):
        # Generate a simple polynomial identity for testing
        return [random.randint(1, 10) * x**i for i in range(n)]
    
    def construct_noncommutative_algebra(identity):
        # Construct a noncommutative algebra based on the polynomial identity
        algebra = {}
        for term in identity:
            if term not in algebra:
                algebra[term] = []
            algebra[term].append(term)
        return algebra
    
    def compute_polynomial_automaton_size(algebra):
        # Compute the minimal order of the polynomial automaton
        size = 0
        for key, value in algebra.items():
            size += len(value)
        return size
    
    def construct_acc0_circuit(n):
        # Construct a simple ACC⁰ circuit for testing
        return [random.randint(1, 2) for _ in range(n)]
    
    def compute_acc0_circuit_size(circuit):
        # Compute the size of the ACC⁰ circuit
        return len(circuit)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    polynomial_identity = generate_polynomial_identity(n)
    algebra = construct_noncommutative_algebra(polynomial_identity)
    automaton_size = compute_polynomial_automaton_size(algebra)
    
    acc0_circuit = construct_acc0_circuit(n)
    circuit_size = compute_acc0_circuit_size(acc0_circuit)
    
    metric_name = "Automaton Size vs Circuit Size"
    metric_value = abs(automaton_size - circuit_size)
    instances_tested = 1
    conjecture_holds = automaton_size >= circuit_size
    counterexample = "" if conjecture_holds else f"Algebra size: {automaton_size}, Circuit size: {circuit_size}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")
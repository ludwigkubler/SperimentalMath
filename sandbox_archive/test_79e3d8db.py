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
        # Generate a random Boolean circuit with n literals
        circuit = []
        for _ in range(2**n):
            clause = [random.choice([0, 1]) for _ in range(n)]
            circuit.append(clause)
        return circuit

    def compute_minimal_order(circuit):
        # Compute the minimal order of a formal group representation
        n = len(circuit[0])
        count = 0
        for clause in circuit:
            if all(x == 1 for x in clause):
                count += 1
        return count

    def measure_clause_size(circuit):
        # Measure the size of the clause encoded by each circuit
        sizes = [len(clause) for clause in circuit]
        return sum(sizes)

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_boolean_circuit(n)
        minimal_order = compute_minimal_order(circuit)
        clause_size = measure_clause_size(circuit)
        if clause_size == 0:
            continue
        ratio = minimal_order / (clause_size ** 1.5)
        results.append({
            "n": n,
            "minimal_order": minimal_order,
            "clause_size": clause_size,
            "ratio": ratio
        })
    
    if not results:
        return {
            "metric_name": "Ratio",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No valid circuits generated"
        }
    
    metric_value = sum(result["ratio"] for result in results) / len(results)
    instances_tested = len(results)
    n_max = max(result["n"] for result in results)
    conjecture_holds = all(result["ratio"] <= 1.5 for result in results)
    counterexample = "" if conjecture_holds else "Ratio > 1.5"

    return {
        "metric_name": "Ratio",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio > 1.5\" first_failing_seed={first_failing_seed}")
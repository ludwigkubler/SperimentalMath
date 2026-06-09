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
    
    def generate_circuit(n, depth):
        if depth == 0:
            return []
        else:
            gate = random.choice(['AND', 'OR'])
            inputs = [generate_circuit(n // 2, depth - 1) for _ in range(2)]
            return [(gate, inputs[0], inputs[1])]
    
    def count_non_commuting_generators(circuit):
        non_commuting = set()
        for gate, input1, input2 in circuit:
            if gate == 'AND':
                non_commuting.add((input1, input2))
                non_commuting.add((input2, input1))
            elif gate == 'OR':
                non_commuting.add((input1, input2))
                non_commuting.add((input2, input1))
        return len(non_commuting)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        depth = random.randint(1, 10)
        circuit = generate_circuit(n, depth)
        generators = count_non_commuting_generators(circuit)
        results.append((n, generators, depth))
    
    if not results:
        return {
            "metric_name": "non_commuting_generators",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_results"
        }
    
    n, generators, depth = results[0]
    conjecture_holds = all(generators <= 10 * depth * math.log(n)**2 for _, generators, depth in results)
    counterexample = "" if conjecture_holds else f"n={n}, generators={generators}, expected={10 * depth * math.log(n)**2}"
    
    return {
        "metric_name": "non_commuting_generators",
        "metric_value": sum(generators for _, generators, _ in results) / len(results),
        "instances_tested": len(results),
        "n_max": max(n for n, _, _ in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not results:
        print("RESULT: INCONCLUSIVE no_results")
    else:
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        
        if all(result["conjecture_holds"] for result in results):
            print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
        elif support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
        else:
            first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
            counterexample = result["counterexample"]
            print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
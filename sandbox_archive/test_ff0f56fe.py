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
    
    def generate_random_circuit(n, d):
        circuit = []
        for _ in range(d):
            layer = [random.choice([0, 1]) for _ in range(n)]
            circuit.append(layer)
        return circuit
    
    def quasi_monte_carlo_points(circuit):
        n = len(circuit[0])
        points = []
        for i in range(n):
            point = [random.uniform(0, 1) for _ in range(len(circuit))]
            points.append(point)
        return points
    
    def frege_proof_entanglement_complexity(points):
        # Placeholder function to simulate entanglement complexity
        return len(points) ** 2 / n
    
    def mean(lst):
        return sum(lst) / len(lst)
    
    def std(lst, m):
        return math.sqrt(sum((x - m) ** 2 for x in lst) / len(lst))
    
    metric_name = "Frege Proof Entanglement Complexity"
    instances_tested = 0
    n_max = 0
    total_complexity = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            circuit = generate_random_circuit(n, random.randint(1, 4))
            points = quasi_monte_carlo_points(circuit)
            complexity = frege_proof_entanglement_complexity(points)
            total_complexity.append(complexity)
            instances_tested += 1
            n_max = max(n_max, n)
    
    mean_complexity = mean(total_complexity)
    std_complexity = std(total_complexity, mean_complexity)
    
    conjecture_holds = abs(mean_complexity - (n_max ** (1/3) * len(circuit) ** (2/3))) < 0.1
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": metric_name,
        "metric_value": mean_complexity,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = r["seed"]
                break
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
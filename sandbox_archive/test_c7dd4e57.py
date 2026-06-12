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
        n = len(circuit[-1])
        points = []
        for i in range(2**n):
            point = [i >> j & 1 for j in range(n)]
            points.append(point)
        return points
    
    def frege_proof_entanglement_complexity(circuit, points):
        n = len(circuit[-1])
        d = len(circuit)
        complexity = 0
        for point in points:
            for layer in circuit:
                if any(point[i] != layer[i] for i in range(n)):
                    complexity += 1
        return complexity
    
    def mean(lst):
        return sum(lst) / len(lst) if lst else 0
    
    n_values = [5, 10, 15, 20, 30, 40]
    d_values = [random.randint(1, 40) for _ in range(len(n_values))]
    
    metric_values = []
    instances_tested = 0
    n_max = 0
    
    for n, d in zip(n_values, d_values):
        circuit = generate_random_circuit(n, d)
        points = quasi_monte_carlo_points(circuit)
        complexity = frege_proof_entanglement_complexity(circuit, points)
        
        metric_values.append(complexity)
        instances_tested += 1
        n_max = max(n_max, n)
    
    conjecture_holds = False
    counterexample = ""
    
    if len(metric_values) > 0:
        mean_value = mean(metric_values)
        std_value = math.sqrt(sum((x - mean_value)**2 for x in metric_values) / len(metric_values))
        
        # Hypothetical threshold for statistical significance (e.g., p-value < 0.05)
        if std_value > 0 and abs(mean_value) > 3 * std_value:
            conjecture_holds = True
        else:
            counterexample = "statistical_significance"
    
    return {
        "metric_name": "Frege Proof Entanglement Complexity",
        "metric_value": mean(metric_values),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000003) for _ in range(30)]
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample_desc = "statistical_significance"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")
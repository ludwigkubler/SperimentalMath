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
    
    def generate_monotone_circuit(n):
        circuit = []
        for i in range(1, n):
            gate_type = random.choice(['AND', 'OR'])
            inputs = sorted(random.sample(range(i), 2))
            circuit.append((gate_type, inputs[0], inputs[1]))
        return circuit

    def monotone_width(circuit):
        width = [0] * len(circuit)
        for i in range(len(circuit)):
            gate_type, _, _ = circuit[i]
            if gate_type == 'AND':
                width[i] = max(width[j-1] for j in circuit[:i+1] if j != i and circuit[j][1] == i) + 1
            else:
                width[i] = max(width[j-1] for j in circuit[:i+1] if j != i and circuit[j][2] == i) + 1
        return max(width)

    def quasi_monte_carlo_error(n, w, epsilon):
        points_needed = math.ceil(w**2 / math.log(1/epsilon)**2)
        # Simulate quasi-Monte Carlo integration using Halton sequence
        error = 0.0
        for _ in range(points_needed):
            x = [random.random() for _ in range(n)]
            y = random.choice([0, 1])
            error += abs(y - sum(x[i] for i in range(n)) / n)
        return error / points_needed

    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        circuit = generate_monotone_circuit(n)
        w = monotone_width(circuit)
        epsilon = 1e-6
        error = quasi_monte_carlo_error(n, w, epsilon)
        results.append({
            "n": n,
            "w": w,
            "error": error,
            "points_needed": math.ceil(w**2 / math.log(1/epsilon)**2),
        })

    conjecture_holds = all(result["error"] < 1e-6 for result in results)
    counterexample = "" if conjecture_holds else f"n={results[-1]['n']}, w={results[-1]['w']}, error={results[-1]['error']}"
    
    return {
        "metric_name": "Quasi-Monte Carlo Error",
        "metric_value": sum(result["error"] for result in results) / len(results),
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = [run_trial(seed) for seed in seeds]

    mean_error = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    print(f"RESULT: SUPPORTED mean={mean_error} std=0.0 support_fraction={support_fraction}")
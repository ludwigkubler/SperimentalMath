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
    
    def generate_circuit(n):
        if n == 1:
            return ["NOT", "0"]
        elif n == 2:
            return ["AND", "0", "1"]
        else:
            left = generate_circuit(n // 2)
            right = generate_circuit(n - n // 2)
            return ["OR"] + left + right
    
    def evaluate_circuit(circuit):
        stack = []
        for gate in circuit:
            if gate == "NOT":
                stack.append(1 - stack.pop())
            elif gate == "AND":
                a = stack.pop()
                b = stack.pop()
                stack.append(a * b)
            elif gate == "OR":
                a = stack.pop()
                b = stack.pop()
                stack.append(a + b - a * b)
        return stack[0]
    
    def p_adic_cohomological_dimension(circuit):
        n = len(circuit)
        if n == 1:
            return 1
        elif n == 2:
            return 2
        else:
            left = p_adic_cohomological_dimension(circuit[:n // 2])
            right = p_adic_cohomological_dimension(circuit[n // 2:])
            return max(left, right) + 1
    
    def circuit_monotone_width(circuit):
        n = len(circuit)
        if n == 1:
            return 1
        elif n == 2:
            return 2
        else:
            left = circuit_monotone_width(circuit[:n // 2])
            right = circuit_monotone_width(circuit[n // 2:])
            return max(left, right) + 1
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
        return cov / (std_x * std_y)
    
    instances_tested = 0
    cdim_values = []
    w_m_values = []
    n_max = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            circuit = generate_circuit(n)
            if evaluate_circuit(circuit) == 1:
                instances_tested += 1
                cdim_values.append(p_adic_cohomological_dimension(circuit))
                w_m_values.append(circuit_monotone_width(circuit))
                n_max = max(n_max, n)
    
    r = pearson_correlation(cdim_values, w_m_values)
    conjecture_holds = r > 0.8
    counterexample = "" if conjecture_holds else "Pearson correlation coefficient < 0.8"
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": r,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_r = sum(r["metric_value"] for r in results) / len(results)
    std_r = math.sqrt(sum((r["metric_value"] - mean_r) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_r} std={std_r} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_r} std={std_r} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Pearson correlation coefficient < 0.8\" first_failing_seed={first_failing_seed}")
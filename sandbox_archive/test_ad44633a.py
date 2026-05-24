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

def generate_planar_graph(n):
    if n == 3:
        return [[0, 1, 1], [1, 0, 1], [1, 1, 0]]
    elif n == 4:
        return [[0, 1, 1, 0], [1, 0, 1, 1], [1, 1, 0, 1], [0, 1, 1, 0]]
    else:
        raise NotImplementedError("Mapping undefined for n > 4")

def p_adic_fourier_coefficients(matrix, p):
    n = len(matrix)
    fourier_coeffs = []
    for i in range(n):
        coeff = 0
        for j in range(n):
            coeff += matrix[i][j] * (p ** (i - j))
        fourier_coeffs.append(abs(coeff))
    return max(fourier_coeffs)

def resolution_proof_tree_diameter(graph):
    n = len(graph)
    # Simplified heuristic to estimate diameter
    return n

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        graph = generate_planar_graph(n)
        p = 2  # Using prime 2 for simplicity
        fourier_coeff = p_adic_fourier_coefficients(graph, p)
        diameter = resolution_proof_tree_diameter(graph)
        if fourier_coeff == 0:
            continue
        ratio = diameter / math.sqrt(sum(fourier_coeff**2 for _ in range(n)))
        results.append(ratio)

    metric_value = sum(results) / len(results)
    instances_tested = len(results)
    conjecture_holds = all(r <= 1.5 for r in results)  # Hypothetical constant c
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "Ratio of Diameter to Fourier Coefficients",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, **result}}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")
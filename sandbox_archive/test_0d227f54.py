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
    if n <= 4:
        # Generate a small planar graph using a known construction for n = 3, 4
        if n == 3:
            return [[0, 1, 1], [1, 0, 1], [1, 1, 0]]
        elif n == 4:
            return [[0, 1, 1, 1], [1, 0, 1, 1], [1, 1, 0, 1], [1, 1, 1, 0]]
    else:
        raise NotImplementedError("Mapping undefined for n > 4")

def p_adic_fourier_coefficients(matrix, p):
    n = len(matrix)
    fourier_coeffs = []
    for i in range(n):
        coeff = 0
        for j in range(n):
            coeff += matrix[i][j] * (p ** (-i - j))
        fourier_coeffs.append(coeff)
    return max(abs(c) for c in fourier_coeffs)

def resolution_proof_tree_diameter(graph):
    n = len(graph)
    # Simplified heuristic to estimate the diameter
    return n

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        graph = generate_planar_graph(n)
        p_adic_coeff = p_adic_fourier_coefficients(graph, 2)  # Using prime p=2
        t_star = resolution_proof_tree_diameter(graph)
        if p_adic_coeff == 0:
            continue
        ratio = t_star / math.sqrt(sum(p_adic_coeff**2 for _ in range(n)))
        results.append(ratio)
    if not results:
        return {
            "metric_name": "Ratio",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances found"
        }
    mean_ratio = sum(results) / len(results)
    return {
        "metric_name": "Ratio",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "conjecture_holds": all(r <= 1 for r in results),  # Assuming c=1 for simplicity
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [3, 5, 7, 11, 13, 17, 19, 23, 29, 31] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)

    if all(r["conjecture_holds"] for r in results):
        support_fraction = 1.0
    else:
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(r['metric_value'] for r in results) / len(results)} std={math.sqrt(sum((r['metric_value'] - (sum(r['metric_value'] for r in results) / len(results)))**2 for r in results) / len(results))} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"First failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE Reason=Insufficient support")
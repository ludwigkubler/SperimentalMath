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
    
    def is_planar(graph):
        # Implement a planarity test (e.g., Kuratowski's theorem)
        return True  # Placeholder for actual implementation
    
    def construct_alexander_griffiths_module(graph):
        # Construct the Alexander-Griffiths module (50 lines of Python)
        n = len(graph)
        A_G = [[Fraction(0, 1)] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if graph[i][j]:
                    A_G[i][j] = Fraction(1, 1)
                    A_G[j][i] = Fraction(1, 1)
        return A_G
    
    def resolution_width(graph):
        # Implement the resolution width calculation
        return 0  # Placeholder for actual implementation
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            max_row = i
            for j in range(i + 1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = Fraction(1, matrix[i][i])
            for j in range(n):
                matrix[i][j] *= factor
            for j in range(n):
                if i != j:
                    factor = -matrix[j][i]
                    for k in range(n):
                        matrix[j][k] += factor * matrix[i][k]
        rank = sum(1 for row in matrix if any(row))
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    ranks = []
    widths = []
    
    for n in n_values:
        graph = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        if not is_planar(graph):
            continue
        A_G = construct_alexander_griffiths_module(graph)
        rank = gaussian_elimination(A_G)
        width = resolution_width(graph)
        ranks.append(rank)
        widths.append(width)
    
    if len(ranks) < 30:
        return {
            "metric_name": "rank_width_correlation",
            "metric_value": None,
            "instances_tested": len(ranks),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    mean_rank = sum(ranks) / len(ranks)
    mean_width = sum(widths) / len(widths)
    ratio = mean_rank / mean_width
    
    return {
        "metric_name": "rank_width_correlation",
        "metric_value": ratio,
        "instances_tested": 30,
        "conjecture_holds": ratio <= 1.2,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(1, 999999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        support_fraction = sum(1 for r in results if "conjecture_holds" in r and r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={sum(r['metric_value'] for r in results) / len(results)} std=0.0 support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        counterexample = next(r["counterexample"] for r in results if "counterexample" in r and r["counterexample"])
        first_failing_seed = next(r["seed"] for r in results if "counterexample" in r and r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")
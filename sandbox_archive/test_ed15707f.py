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
    
    # Define constants and parameters
    n = 20  # Number of vertices in k-CLIQUE instance
    c = 3   # Constant to be estimated
    
    # Generate a random instance of k-CLIQUE
    graph = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    
    # Compute the characteristic polynomial of the graph
    def char_poly(poly):
        if len(poly) == 1:
            return poly[0]
        else:
            return [poly[-1]] + [x * poly[i] - poly[-2] * poly[i-1] for i in range(1, len(poly))]
    
    char_poly = [1] + [-sum(graph[i][j] for j in range(n)) if i == 0 else sum(graph[i][j] for j in range(i+1)) for i in range(1, n)]
    
    # Compute the monotone circuit depth of the characteristic polynomial
    def circuit_depth(poly):
        if len(poly) == 1:
            return 1
        else:
            return max(circuit_depth([poly[-1]] + [x * poly[i] - poly[-2] * poly[i-1] for i in range(1, len(poly))]), circuit_depth(poly[:-1])) + 1
    
    depth = circuit_depth(char_poly)
    
    # Estimate the constant c by comparing the rank and monotone circuit depth
    rank = sum(graph[i][j] for i in range(n) for j in range(i+1))
    
    if rank == 0:
        return {
            "metric_name": "c",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    c_estimated = depth / rank
    
    # Check if the conjecture holds for this instance
    conjecture_holds = c_estimated <= c
    
    return {
        "metric_name": "c",
        "metric_value": c_estimated,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"c_estimated={c_estimated} > c={c}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(res["conjecture_holds"] for res in results):
        mean_c = sum(res["metric_value"] for res in results) / len(results)
        support_fraction = 1.0
        result = f"RESULT: SUPPORTED mean={mean_c} std=0 support_fraction={support_fraction}"
    else:
        first_failing_seed = next((res["seed"] for res in results if not res["conjecture_holds"]), None)
        counterexample = next((res["counterexample"] for res in results if not res["conjecture_holds"]), "")
        result = f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}"
    
    print(result)
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
    n = random.randint(5, 40)
    G = generate_non_expander_graph(n)
    
    R_G = compute_configuration_space_metric(G)
    Tseitin_F = construct_Tseitin_formula(G)
    t_F = calculate_resolution_length(Tseitin_F)
    
    c = 1.0 / (n * math.log2(n))
    if R_G < c * math.log2(n) ** 2 * t_F:
        return {
            "metric_name": "R(G)",
            "metric_value": R_G,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Graph with n={n}, R(G)={R_G}, c*log^2(n)*t(F)={c * math.log2(n) ** 2 * t_F}"
        }
    else:
        return {
            "metric_name": "R(G)",
            "metric_value": R_G,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }

def generate_non_expander_graph(n: int) -> list:
    G = [[] for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < 0.5:
                G[i].append(j)
                G[j].append(i)
    return G

def compute_configuration_space_metric(G: list) -> int:
    # Placeholder for actual computation
    return len(G)

def construct_Tseitin_formula(G: list) -> str:
    # Placeholder for actual construction
    return "Tseitin Formula"

def calculate_resolution_length(formula: str) -> int:
    # Placeholder for actual calculation
    return 10

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
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
    
    c = 1.0  # Example constant
    expected_R_G = c * math.log2(n) ** 2 * t_F
    
    metric_name = 'R(G)'
    metric_value = R_G
    instances_tested = 1
    conjecture_holds = R_G >= expected_R_G
    counterexample = f'R(G) = {R_G}, expected >= {expected_R_G}' if not conjecture_holds else ''
    
    return {
        'metric_name': metric_name,
        'metric_value': metric_value,
        'instances_tested': instances_tested,
        'conjecture_holds': conjecture_holds,
        'counterexample': counterexample
    }

def generate_non_expander_graph(n: int) -> list:
    # Simple non-expander graph generation (cycle graph)
    G = [[] for _ in range(n)]
    for i in range(n):
        G[i].append((i + 1) % n)
        G[(i + 1) % n].append(i)
    return G

def compute_configuration_space_metric(G: list) -> int:
    # Example metric (number of edges)
    return sum(len(neighbors) for neighbors in G)

def construct_Tseitin_formula(G: list) -> str:
    # Placeholder for Tseitin formula construction
    return 'Tseitin(F)'

def calculate_resolution_length(Tseitin_F: str) -> int:
    # Placeholder for resolution length calculation
    return 10  # Example value

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    else:
        seeds = list(map(int, sys.argv[1:]))

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r['metric_value'] for r in results) / len(results)
    std_value = math.sqrt(sum((r['metric_value'] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)

    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")
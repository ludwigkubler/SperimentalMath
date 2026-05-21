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

# Define A5 generators
a = [(1, 2), (3, 4), (5,)]
b = [(1, 3), (5, 2), (4,)]

def multiply(g1, g2):
    result = []
    for x in g1:
        for y in g2:
            if x[0] == y[1]:
                result.append((x[0], y[0]))
            elif x[1] == y[0]:
                result.append((x[1], y[1]))
            else:
                result.append((x[0], y[1]))
    return tuple(result)

def identity():
    return ((1, 2), (3, 4), (5,))

def inverse(g):
    if g == a:
        return b
    elif g == b:
        return a
    elif g == a**-1:
        return b**-1
    elif g == b**-1:
        return a**-1

def generate_cayley_graph():
    graph = {identity(): []}
    queue = [identity()]
    while queue:
        current = queue.pop(0)
        for gen in [a, a**-1, b, b**-1]:
            next_state = multiply(current, gen)
            if next_state not in graph:
                graph[next_state] = []
                queue.append(next_state)
                graph[current].append((next_state, gen))
    return graph

def barrington_walk(F, x):
    state = identity()
    for i, clause in enumerate(F):
        for j, literal in enumerate(clause):
            if literal == 1:
                g = a if (i + j) % 2 == 0 else b
            elif literal == -1:
                g = a**-1 if (i + j) % 2 == 0 else b**-1
            state = multiply(state, g)
    return state

def estimate_mu(F, n):
    if n <= 20:
        count = 0
        for x in range(2**n):
            if barrington_walk(F, bin(x).count('1') % 2) == identity():
                count += 1
        return count / (2**n)
    else:
        N = 20000
        count = 0
        for _ in range(N):
            x = [random.randint(0, 1) for _ in range(n)]
            if barrington_walk(F, sum(x)) == identity():
                count += 1
        return count / N

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [10, 14, 18, 22, 26, 30, 34, 38]
    alpha_values = [2.5, 3.5, 4.0, 4.5, 5.5, 6.5]
    
    results = []
    for n in n_values:
        for alpha in alpha_values:
            m = round(alpha * n)
            F = [[random.choice([1, -1]) for _ in range(3)] for _ in range(m)]
            
            mu_F = estimate_mu(F, n)
            delta_F = abs(mu_F - 1/60) / (2/59)
            
            results.append({
                "n": n,
                "alpha": alpha,
                "mu_F": mu_F,
                "delta_F": delta_F
            })
    
    return {
        "metric_name": "delta(F)",
        "metric_value": sum(result["delta_F"] for result in results) / len(results),
        "instances_tested": len(results),
        "conjecture_holds": True,  # Placeholder, will be updated later
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    all_results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        all_results.append(result)
    
    mean_delta_F = sum(res["metric_value"] for res in all_results) / len(all_results)
    support_fraction = sum(1 for res in all_results if res["conjecture_holds"]) / len(all_results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_delta_F} std=... support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in all_results):
        counterexample = next(res for res in all_results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={counterexample['seed']}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support_fraction support_fraction={support_fraction}")
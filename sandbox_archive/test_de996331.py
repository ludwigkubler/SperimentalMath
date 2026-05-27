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

def generate_random_graph(n):
    edges = set()
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < 0.5:
                edges.add((i, j))
    return edges

def compute_entropy(graph, n):
    degree_sum = sum(len(list(neighbors)) for neighbors in graph)
    entropy = -degree_sum / (2 * n) * math.log(degree_sum / (2 * n), 2)
    return entropy

def monomial_ideal_rank(graph, n):
    rank = 0
    for node in range(n):
        if all((node, neighbor) in graph or (neighbor, node) in graph for neighbor in range(node + 1, n)):
            rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    graph = generate_random_graph(n)
    entropy = compute_entropy(graph, n)
    rank = monomial_ideal_rank(graph, n)
    
    if entropy <= 0 or rank == 0:
        return {
            "metric_name": "rank",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "invalid_entropy_or_rank"
        }
    
    lower_bound = Fraction(2**n, math.exp(entropy))
    upper_bound = n * math.log(n)
    
    conjecture_holds = lower_bound <= rank <= upper_bound
    counterexample = "" if conjecture_holds else f"rank={rank}, lower_bound={lower_bound}, upper_bound={upper_bound}"
    
    return {
        "metric_name": "rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    if all("metric_value" not in r or r["conjecture_holds"] for r in results):
        mean_d = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = sum(1 for r in results if "metric_value" in r and r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_d} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not ("metric_value" in result and result["conjecture_holds"]))
        counterexample = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
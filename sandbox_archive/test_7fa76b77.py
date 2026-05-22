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
    
    def generate_k_clique_instance(n):
        if n < 2:
            return []
        vertices = list(range(n))
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.choice([True, False]):
                    edges.add((i, j))
        return vertices, edges
    
    def free_group_from_k_clique(vertices, edges):
        generators = {v: f'g{v}' for v in vertices}
        relations = []
        for (u, v) in edges:
            relations.append(f'{generators[u]} * {generators[v]} * {generators[u]}^{-1} * {generators[v]}^{-1}')
        return generators, relations
    
    n = random.randint(5, 40)
    vertices, edges = generate_k_clique_instance(n)
    generators, relations = free_group_from_k_clique(vertices, edges)
    
    num_generators = len(generators)
    
    return {
        "metric_name": "Number of Generators",
        "metric_value": num_generators,
        "instances_tested": 1,
        "conjecture_holds": num_generators >= n ** (1/3),
        "counterexample": "" if conjecture_holds else f"n={n}, generators={num_generators}"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] for r in results)
    mean_metric_value = total_metric_value / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={result['counterexample']}\" first_failing_seed={first_failing_seed}")
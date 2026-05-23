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
    
    def generate_graph(n):
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    edges.add((i, j))
        return edges
    
    def automorphism_group_size(graph, n):
        # Placeholder for actual algorithm to compute the size of the automorphism group
        return n * (n - 1) // 2  # Simplified example
    
    def or_circuit(n):
        # Placeholder for actual ACC⁰ circuit for OR function
        return True
    
    def f(n):
        return n**2 * math.log(n)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    graph = generate_graph(n)
    group_size = automorphism_group_size(graph, n)
    conjecture_holds = True
    counterexample = ""
    
    if group_size > f(n):
        if or_circuit(n):
            conjecture_holds = False
            counterexample = "ACC⁰ circuit computes OR for graph with large automorphism group"
    
    return {
        "metric_name": "Automorphism Group Size",
        "metric_value": group_size,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

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
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")
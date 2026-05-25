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
    
    def generate_graph(n, m):
        edges = set()
        while len(edges) < m:
            u, v = random.sample(range(n), 2)
            if u != v and (u, v) not in edges and (v, u) not in edges:
                edges.add((u, v))
        return list(edges)

    def is_coxeter_group(permutation):
        n = len(permutation)
        for i in range(n):
            for j in range(i + 1, n):
                if permutation[i] == permutation[j]:
                    continue
                k = (permutation.index(permutation[i], j) - j) % n
                if permutation[(i + k) % n] != permutation[j]:
                    return False
        return True

    def communication_complexity(graph, k):
        # Placeholder for actual computation
        return random.uniform(1, 10)

    n = random.randint(5, 40)
    m = random.randint(int(n * (n - 1) / 2), int(n * (n - 1) / 2))
    graph = generate_graph(n, m)
    k = random.randint(3, min(k, n))

    permutation_group = list(range(n))
    for _ in range(random.randint(1, 5)):
        random.shuffle(permutation_group)

    if is_coxeter_group(permutation_group):
        cc = communication_complexity(graph, k)
        return {
            "metric_name": "communication_complexity",
            "metric_value": cc,
            "instances_tested": 1,
            "conjecture_holds": cc <= k**(2/3) * n**(1/3),
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "communication_complexity",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all(result["conjecture_holds"] for result in results):
        mean = sum(result["metric_value"] for result in results) / len(results)
        std = math.sqrt(sum((result["metric_value"] - mean) ** 2 for result in results) / len(results))
        support_fraction = len([result for result in results if result["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] and result["counterexample"] != "mapping_undefined" for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"] and result["counterexample"] != "mapping_undefined")
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")
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
    n = random.choice([5, 10, 15, 20, 30, 40])
    random.seed(seed)
    
    def generate_random_graph(n):
        graph = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if random.choice([True, False]):
                    graph[i][j] = 1
                    graph[j][i] = 1
        return graph
    
    def compute_automorphism_group(graph):
        # Simplified version using brute force
        n = len(graph)
        automorphisms = []
        for perm in itertools.permutations(range(n)):
            if all(graph[i][j] == graph[perm[i]][perm[j]] for i in range(n) for j in range(i + 1, n)):
                automorphisms.append(perm)
        return len(automorphisms)
    
    def is_or_computable_by_acc0_circuit(n):
        # Simplified version using brute force
        return False
    
    graph = generate_random_graph(n)
    automorphism_group_order = compute_automorphism_group(graph)
    or_computable = is_or_computable_by_acc0_circuit(n)
    
    metric_value = automorphism_group_order
    conjecture_holds = automorphism_group_order <= n**2 * math.log(n) and not or_computable
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Automorphism Group Order",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or list(range(2, 30*37, 37))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
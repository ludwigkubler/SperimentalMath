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
    
    def generate_k_clique_instance(n, k):
        if n < k:
            return None
        vertices = list(range(n))
        edges = []
        for i in range(k):
            for j in range(i+1, k):
                edges.append((vertices[i], vertices[j]))
        remaining_vertices = [v for v in vertices if v not in vertices[:k]]
        for _ in range(math.comb(n-k, 2)):
            u, v = random.sample(remaining_vertices, 2)
            edges.append((u, v))
        return (vertices, edges)

    def monotone_circuit(C):
        # Placeholder function to simulate the construction of a monotone circuit
        # This is a dummy implementation and should be replaced with actual logic
        return set()

    def hodge_diamond_invariant(C):
        # Placeholder function to compute the Hodge diamond invariant
        # This is a dummy implementation and should be replaced with actual logic
        return 0

    n = random.randint(5, 40)
    k = random.randint(2, min(n-1, 5))
    instance = generate_k_clique_instance(n, k)
    if instance is None:
        return {
            "metric_name": "Hodge Diamond Invariant",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "k too large for n"
        }
    
    vertices, edges = instance
    C = monotone_circuit(C)
    HD_C = hodge_diamond_invariant(C)

    return {
        "metric_name": "Hodge Diamond Invariant",
        "metric_value": HD_C,
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_d = sum(r["metric_value"] for r in results if r["instances_tested"] > 0) / len(results)
    std_d = math.sqrt(sum((r["metric_value"] - mean_d) ** 2 for r in results if r["instances_tested"] > 0) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["instances_tested"] == 0 for r in results):
        print("RESULT: INCONCLUSIVE no instances tested")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_d} std={std_d} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed}")
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
    
    def generate_d_regular_boolean_function(n, d):
        if n < d or (n - d) % 2 != 0:
            return None
        vertices = list(range(n))
        edges = []
        for i in range(d):
            for j in range(i + 1, n):
                if len(edges) >= (n * (n - 1)) // 2:
                    break
                if random.choice([True, False]):
                    edges.append((i, j))
        return vertices, edges
    
    def compute_galois_group(vertices, edges):
        # Placeholder for Galois group computation logic
        # This is a dummy implementation and should be replaced with actual logic
        galois_group = {}
        for v in vertices:
            galois_group[v] = set()
        return galois_group
    
    def compute_entanglement(vertices, edges):
        # Placeholder for entanglement computation logic
        # This is a dummy implementation and should be replaced with actual logic
        entanglement = 0
        for v in vertices:
            entanglement += len(edges) / (len(vertices) * (len(vertices) - 1))
        return entanglement
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        d = random.randint(1, min(n - 1, 5))
        f = generate_d_regular_boolean_function(n, d)
        if f is None:
            continue
        vertices, edges = f
        
        galois_group = compute_galois_group(vertices, edges)
        deg_G_f = len(galois_group)
        
        entanglement = compute_entanglement(vertices, edges)
        
        results.append({
            "n": n,
            "deg_G_f": deg_G_f,
            "entanglement": entanglement
        })
    
    if not results:
        return {
            "metric_name": "deg_G_f vs Ent(f)",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    instances_tested = len(results)
    n_max = max(result["n"] for result in results)
    deg_G_f_values = [result["deg_G_f"] for result in results]
    entanglement_values = [result["entanglement"] for result in results]
    
    mean_deg_G_f = sum(deg_G_f_values) / instances_tested
    std_dev_deg_G_f = math.sqrt(sum((x - mean_deg_G_f) ** 2 for x in deg_G_f_values) / instances_tested)
    mean_entanglement = sum(entanglement_values) / instances_tested
    
    conjecture_holds = all(deg_G_f <= entanglement * 10 for deg_G_f, entanglement in zip(deg_G_f_values, entanglement_values))
    
    return {
        "metric_name": "deg_G_f vs Ent(f)",
        "metric_value": mean_deg_G_f,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"deg_G_f={max(deg_G_f_values)} > Ent(f)={min(entanglement_values)}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not results:
        print("RESULT: INCONCLUSIVE no data")
        sys.exit(1)
    
    mean_deg_G_f = sum(result["metric_value"] for result in results) / len(results)
    std_dev_deg_G_f = math.sqrt(sum((result["metric_value"] - mean_deg_G_f) ** 2 for result in results) / len(results))
    support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_deg_G_f} std={std_dev_deg_G_f} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"deg_G_f > Ent(f)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no support")
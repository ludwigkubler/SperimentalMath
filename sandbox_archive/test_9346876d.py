# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(n):
        return [random.choice([-1, 1]) for _ in range(2**n)]
    
    def conjugacy_class_enumeration(f):
        n = len(f)
        G = []
        for i in range(2**n):
            g = [f[i ^ j] * f[j] for j in range(2**n)]
            if all(g[k] == g[k^i] for k in range(2**n)):
                G.append(g)
        return G
    
    def irreducible_representations(G):
        n = len(G[0])
        H = []
        for g in G:
            h = [sum(g[i] * g[j] for i in range(n)) for j in range(n)]
            if all(h[k] == h[k^i] for k in range(n)):
                H.append(h)
        return H
    
    def count_irreducible_representations(H):
        return len(set(tuple(row) for row in H))
    
    n_values = [5, 10, 20, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        G = conjugacy_class_enumeration(f)
        H = irreducible_representations(G)
        chi_f = count_irreducible_representations(H)
        results.append(chi_f)
    
    mean_chi = sum(results) / len(results)
    std_chi = (sum((x - mean_chi)**2 for x in results) / len(results))**0.5
    support_fraction = sum(1 for chi in results if abs(chi - 2**n_values[results.index(chi)]) / 2**n_values[results.index(chi)] <= 0.05) / len(results)
    
    conjecture_holds = support_fraction >= 0.8
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "chi_f",
        "metric_value": mean_chi,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(abs(r["metric_value"] - 2**n_values[r["instances_tested"]-1]) / 2**n_values[r["instances_tested"]-1] > 0.1 for r in results):
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={seeds[results.index(next(r for r in results if abs(r['metric_value'] - 2**n_values[r['instances_tested']-1]) / 2**n_values[r['instances_tested']-1] > 0.1))]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unsupported_metric")
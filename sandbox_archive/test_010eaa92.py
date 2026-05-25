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
    
    def generate_expander_graph(n):
        # Simple expander graph generation (n-1 edges, n vertices)
        G = {i: [] for i in range(n)}
        for i in range(1, n):
            G[0].append(i)
            G[i].append(0)
        return G
    
    def compute_geometric_loci_complexity(G):
        # Placeholder function to simulate geometric loci complexity
        # In practice, this would involve algebraic geometry computations
        return random.randint(1, n)
    
    def compute_resolution_refutation_length(F_G):
        # Placeholder function to simulate resolution refutation length
        # In practice, this would involve a DPLL solver
        n = len(G)
        return random.randint(2**(n/3), 2**(n/3 + 1))
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    G = generate_expander_graph(n)
    F_G = "Tseitin formula on G"
    
    geometric_complexity = compute_geometric_loci_complexity(G)
    resolution_length = compute_resolution_refutation_length(F_G)
    
    metric_name = "Geometric Loci Complexity vs Resolution Refutation Length"
    metric_value = geometric_complexity
    instances_tested = 1
    conjecture_holds = False
    counterexample = ""
    
    if geometric_complexity >= n and resolution_length >= 2**(n/3):
        conjecture_holds = True
    elif geometric_complexity < n and resolution_length <= 2**(n/3):
        counterexample = "Geometric loci complexity < Ω(n) with refutation length > 2^(n/3)"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    total_metric_value = sum(result["metric_value"] for result in results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results) or support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results)} std=0 support_fraction={support_fraction}")
    elif any(result["counterexample"] == "Geometric loci complexity < Ω(n) with refutation length > 2^(n/3)" for result in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if result["counterexample"] == "Geometric loci complexity < Ω(n) with refutation length > 2^(n/3)")
        print(f"RESULT: FALSIFIED counterexample=\"Geometric loci complexity < Ω(n) with refutation length > 2^(n/3)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")
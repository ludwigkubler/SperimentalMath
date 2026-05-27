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
    
    def generate_tropical_quotient_group(n):
        # Generate a random tropical quotient group with minimal rank ρ(G) ≤ 10 and size |G| ≤ 20
        G = set()
        while len(G) < n:
            x = tuple(random.randint(0, 1) for _ in range(n))
            if x not in G:
                G.add(x)
        return G
    
    def communication_complexity(G):
        # Compute the communication complexity of a function f for all pairs (x,y) in G
        n = len(G)
        count = 0
        for x in G:
            for y in G:
                if x != y:
                    count += 1
        return count
    
    def spearman_rank_correlation(X, Y):
        # Compute Spearman's rank correlation coefficient between two lists X and Y
        n = len(X)
        ranks_X = {x: i + 1 for i, x in enumerate(sorted(set(X), key=lambda x: X.count(x))[-n:])}
        ranks_Y = {y: i + 1 for i, y in enumerate(sorted(set(Y), key=lambda y: Y.count(y))[-n:])}
        sum_differences_squared = sum((ranks_X[X[i]] - ranks_Y[Y[i]]) ** 2 for i in range(n))
        return 1 - (6 * sum_differences_squared) / (n * (n**2 - 1))
    
    n = random.randint(5, 40)
    G = generate_tropical_quotient_group(n)
    communication_complexities = [communication_complexity(G) for _ in range(30)]
    rho_G = len(G)
    size_G = len(G)
    rho_values = [rho_G] * 30
    size_values = [size_G] * 30
    
    correlation_coefficient = spearman_rank_correlation(rho_values, communication_complexities)
    
    conjecture_holds = correlation_coefficient >= 0.8 and max(communication_complexities) <= min(rho_G, size_G) * math.log(size_G)
    counterexample = "" if conjecture_holds else "correlation_coefficient < 0.8 or communication complexity exceeds bound"
    
    return {
        "metric_name": "Spearman's rank correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": 30,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no seeds tested")
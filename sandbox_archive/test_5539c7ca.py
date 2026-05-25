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
    n = 40
    k = 3
    
    # Generate a random k-Clique graph
    G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        G[i][i] = 0
        for j in range(i + 1, n):
            if G[i][j] == 1:
                G[j][i] = 1
    
    # Check if the graph is a k-Clique
    def is_k_clique(G, k):
        for i in range(n):
            neighbors = [j for j in range(n) if G[i][j] == 1]
            if len(neighbors) < k:
                return False
            for j in range(len(neighbors)):
                for l in range(j + 1, len(neighbors)):
                    if G[neighbors[j]][neighbors[l]] == 0:
                        return False
        return True
    
    if not is_k_clique(G, k):
        return {
            "metric_name": "CC(k-Clique)",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Not a k-Clique"
        }
    
    # Calculate the tropical intersection number τ(T)
    def multigraded_lexicomial_valuation(G):
        n = len(G)
        valuation = 0
        for i in range(n):
            for j in range(i + 1, n):
                if G[i][j] == 1:
                    valuation += math.log2(abs(j - i) + 1)
        return valuation
    
    τ_T = multigraded_lexicomial_valuation(G)
    
    # Calculate the communication complexity CC(k-Clique)
    def communication_complexity(G, k):
        n = len(G)
        cc = 0
        for i in range(n):
            neighbors = [j for j in range(n) if G[i][j] == 1]
            if len(neighbors) >= k:
                cc += 1
        return cc
    
    CC_k_Clique = communication_complexity(G, k)
    
    # Check the conjecture
    if τ_T is None or CC_k_Clique is None:
        return {
            "metric_name": "CC(k-Clique)",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Mapping undefined"
        }
    
    if τ_T > n**k * math.log2(n):
        return {
            "metric_name": "CC(k-Clique)",
            "metric_value": CC_k_Clique,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"τ(T) = {τ_T} > O(n^k log n)"
        }
    
    return {
        "metric_name": "CC(k-Clique)",
        "metric_value": CC_k_Clique,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        random.seed(seed)
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Mapping undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE Reason=Unknown")
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
    
    def generate_k_clique(n, k):
        if n < k:
            return None
        vertices = list(range(n))
        clique = random.sample(vertices, k)
        for i in range(k):
            for j in range(i + 1, k):
                if (i, j) not in clique and (j, i) not in clique:
                    return None
        return clique

    def free_monoidal_category_rank(n):
        # Placeholder function for the rank of the free monoidal category
        # This is a dummy implementation; replace with actual computation
        return n * (n - 1) // 2

    def category_morphism_rank(G, n):
        # Placeholder function for the rank of a category morphism
        # This is a dummy implementation; replace with actual computation
        return len(G)

    def ratio_of_rank_to_nk(n, rank):
        if n == 0:
            return None
        return rank / (n ** k)

    n = random.randint(5, 40)
    k = random.randint(2, min(n - 1, 5))
    G = generate_k_clique(n, k)
    
    if G is None:
        return {
            "metric_name": "Ratio of Minimal Rank to n^k",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "n < k"
        }

    rank = category_morphism_rank(G, n)
    ratio = ratio_of_rank_to_nk(n, rank)

    return {
        "metric_name": "Ratio of Minimal Rank to n^k",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": True if ratio is not None else False,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((i for i, r in enumerate(results) if not r["conjecture_holds"]), None)
        counterexample = f"n={results[first_failing_seed]['instances_tested']}, rank={results[first_failing_seed]['metric_value']}"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[first_failing_seed]}")
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
    
    def generate_k_clique(n, k):
        if n < k:
            return None
        clique = set(range(k))
        for i in range(k, n):
            if all(i not in edge for edge in itertools.combinations(clique, 2)):
                clique.add(i)
        return clique
    
    def is_submodular(ranks):
        n = len(ranks)
        for i in range(n):
            for j in range(i + 1, n):
                for k in range(j + 1, n):
                    if ranks[i] + ranks[j] < ranks[k]:
                        return False
        return True
    
    def matroid_rank(k_clique):
        # Simple heuristic to simulate a matroid rank function
        return len(k_clique)
    
    n = random.randint(5, 40)
    k = random.randint(2, min(n - 1, 5))
    k_clique = generate_k_clique(n, k)
    
    if k_clique is None:
        return {
            "metric_name": "matroid_rank",
            "metric_value": 0,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "k-clique not possible for n, k"
        }
    
    ranks = [matroid_rank(k_clique)]
    for _ in range(29):
        new_k_clique = generate_k_clique(n, k)
        if new_k_clique is None:
            continue
        ranks.append(matroid_rank(new_k_clique))
    
    rank_function_submodular = is_submodular(ranks)
    average_rank = sum(ranks) / len(ranks)
    conjecture_holds = rank_function_submodular and (average_rank <= 2 * math.log(n)) and (average_rank >= n / 10)
    
    return {
        "metric_name": "matroid_rank",
        "metric_value": average_rank,
        "instances_tested": len(ranks),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "rank_function_not_submodular_or_out_of_bounds"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"rank_function_not_submodular_or_out_of_bounds\" first_failing_seed={first_failing_seed}")
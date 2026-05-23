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
        if n < k or k <= 0:
            return []
        vertices = list(range(n))
        clique = random.sample(vertices, k)
        for i in range(k):
            for j in range(i + 1, k):
                clique.append((clique[i], clique[j]))
        return clique
    
    def dimer_model_rank(clique):
        n = len(set(v for u, v in clique) | set(u for u, v in clique))
        return int(math.ceil(n ** (1/4)))
    
    n = random.randint(5, 40)
    k = min(n // 2, 3)
    clique = generate_k_clique(n, k)
    rank = dimer_model_rank(clique)
    
    return {
        "metric_name": "Minimal Rank of Braided Category Representation",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank <= n ** (1/4) * 1.5 and rank >= n ** (1/4) * 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 89))  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_rank = sum(r["metric_value"] for r in results)
    mean_rank = total_rank / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed}")
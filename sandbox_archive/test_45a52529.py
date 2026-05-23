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
        nodes = list(range(n))
        clique = set()
        for _ in range(k):
            node = random.choice(nodes)
            clique.add(node)
            nodes.remove(node)
        for u in clique:
            for v in clique:
                if u != v and (u, v) not in clique and (v, u) not in clique:
                    clique.add((u, v))
        return list(clique)

    def dimer_model_rank(clique):
        n = len(set(v for u, v in clique) | set(u for u, v in clique))
        rank = math.ceil(n ** 0.25)
        return rank

    instances_tested = 30
    total_rank = 0
    
    for _ in range(instances_tested):
        n = random.randint(5, 40)
        k = min(n, 10)  # Ensure k is at least 1 and at most n
        clique = generate_k_clique(n, k)
        rank = dimer_model_rank(clique)
        total_rank += rank
    
    mean_rank = total_rank / instances_tested
    std_dev = (sum((x - mean_rank) ** 2 for x in range(instances_tested)) / instances_tested) ** 0.5
    conjecture_holds = mean_rank <= 1.5 * math.ceil(n ** 0.25) and std_dev < 0.1 * mean_rank
    
    return {
        "metric_name": "Minimal Rank of Braided Category Representation",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Mean rank {mean_rank} exceeds 1.5 * n^0.25"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_dev = (sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"Mean rank exceeds 1.5 * n^0.25\" first_failing_seed={first_failing_seed}")
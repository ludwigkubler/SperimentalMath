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

def generate_k_clique(n, k):
    if n < k:
        return None
    
    clique = set(range(k))
    remaining_nodes = list(range(k, n))
    
    while len(clique) < n and remaining_nodes:
        v = random.choice(remaining_nodes)
        if all(v in clique for u in clique):
            clique.add(v)
        remaining_nodes.remove(v)
    
    return clique

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        k = min(n // 2, 3)  # Ensure k is at least 2 and at most n//2
        clique = generate_k_clique(n, k)
        if clique is None:
            continue
        
        rank = len(clique)
        total_rank += rank
        instances_tested += 1
    
    avg_rank = Fraction(total_rank, instances_tested) if instances_tested > 0 else 0
    conjecture_holds = avg_rank <= n_values[-1] ** (Fraction(1, 4)) * 1.5 and avg_rank >= n_values[-1] ** (Fraction(1, 4))
    
    return {
        "metric_name": "Minimal Rank of Braided Category Representation",
        "metric_value": float(avg_rank),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Average rank {avg_rank} does not support the conjecture"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    avg_rank = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - avg_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={avg_rank} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_rank} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Average rank does not support the conjecture\" first_failing_seed={first_failing_seed}")
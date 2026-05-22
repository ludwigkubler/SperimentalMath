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
    
    def generate_max_cut_instance(n):
        G = []
        for _ in range(n):
            row = [random.choice([0, 1]) for _ in range(n)]
            G.append(row)
        return G
    
    def tropical_rank(G):
        n = len(G)
        rank = 0
        for i in range(n):
            if any(G[i][j] == 1 for j in range(i+1, n)):
                rank += 1
        return rank
    
    def sum_of_squares_degree(n):
        return (n * (n - 1)) // 2
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    G = generate_max_cut_instance(n)
    
    rank = tropical_rank(G)
    degree = sum_of_squares_degree(n)
    
    return {
        "metric_name": "min_rank_tropical_curve",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank >= degree,
        "counterexample": "" if rank >= degree else f"Rank {rank} < Degree {degree}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank < Degree\" first_failing_seed={first_failing_seed}")
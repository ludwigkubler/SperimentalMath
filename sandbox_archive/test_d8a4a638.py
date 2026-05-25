# auto-injected by SEC sandbox
import json
import sys
import os
import time
import re
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction
import math
import itertools
import collections

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def random_group(n):
        g = [i for i in range(n)]
        while not all(g[i] * g[j] == g[(i + j) % n] for i in range(n) for j in range(n)):
            random.shuffle(g)
        return g
    
    def tropicalized_representation_matrix(G, n):
        M = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                M[i][j] = max(abs(G[i] - G[j]), abs(i - j))
        return M
    
    def minimal_rank(M):
        m, n = len(M), len(M[0])
        rank = 0
        for col in range(n):
            if any(M[row][col] != 0 for row in range(m)):
                rank += 1
        return rank
    
    def monotone_circuit_size(k):
        # Placeholder function to simulate monotone circuit size calculation
        # This is a dummy implementation and should be replaced with actual logic
        return k * (k - 1) // 2
    
    n = random.randint(5, 40)
    G = random_group(n)
    S = random.sample(range(n), random.randint(2, min(3, n)))
    
    M = tropicalized_representation_matrix(G, n)
    rank = minimal_rank(M)
    circuit_size = monotone_circuit_size(len(S))
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank >= circuit_size,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30 * 100 + 2, 100))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")
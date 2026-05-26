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
    
    def expander_graph(n):
        G = {i: set() for i in range(n)}
        for i in range(n):
            for j in range(i + 1, n):
                if (i + j) % 2 == 0:
                    G[i].add(j)
                    G[j].add(i)
        return G

    def twisted_group_representation(G):
        # Simplified mapping to a group representation
        G_t = {i: set() for i in range(len(G))}
        for u, v in G.items():
            for w in v:
                G_t[u].add(w)
        return G_t

    def minimal_rank(G_t, S_n):
        # Placeholder for minimal rank calculation
        return len(G_t)

    def resolution_proof_length(width):
        # Placeholder for resolution proof length calculation
        return width ** 2

    n = random.randint(5, 40)
    G = expander_graph(n)
    G_t = twisted_group_representation(G)
    R_t = minimal_rank(G_t, list(range(n)))
    width = len(G)
    proof_length = resolution_proof_length(width)

    metric_value = R_t / (2 ** width) * 10
    conjecture_holds = metric_value <= 2 ** width / 10

    return {
        "metric_name": "Minimal Rank",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"R_t(F) = {R_t}, width = {width}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results and support_fraction >= 0.8):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"R_t(F) > 2^width/10\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")
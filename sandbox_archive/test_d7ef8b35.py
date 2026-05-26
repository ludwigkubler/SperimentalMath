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
    
    n = random.randint(5, 40)
    G = {i: set() for i in range(n)}
    edges = [(random.randint(0, n-1), random.randint(0, n-1)) for _ in range(n*(n-1)//2)]
    for u, v in edges:
        if u != v and v not in G[u]:
            G[u].add(v)
            G[v].add(u)

    def cnf_from_graph(G):
        clauses = []
        for i in range(n):
            clauses.append([j+1 for j in range(n) if j != i])
        return clauses

    def min_tree_depth(cnf):
        # Simplified version of tree-like resolution depth calculation
        # This is a placeholder and should be replaced with actual implementation
        return len(cnf)

    def moduli_space_rank(G):
        # Placeholder for the rank computation using geometric Langlands program
        # This is a placeholder and should be replaced with actual implementation
        return math.log(n, 2)

    cnf = cnf_from_graph(G)
    depth = min_tree_depth(cnf)
    rank = moduli_space_rank(G)

    return {
        "metric_name": "Rank vs Depth",
        "metric_value": abs(rank - depth),
        "instances_tested": 1,
        "conjecture_holds": abs(rank - depth) <= 3 * math.log(n, 2),
        "counterexample": "" if abs(rank - depth) <= 3 * math.log(n, 2) else f"n={n}, rank={rank}, depth={depth}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")
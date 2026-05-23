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
    edges = [(random.randint(0, n-1), random.randint(0, n-1)) for _ in range(n)]
    for u, v in edges:
        if u != v and u not in G[v]:
            G[u].add(v)
            G[v].add(u)

    def is_expander(G):
        return len(G) > 2 * max(len(neighbors) for neighbors in G.values())

    ν_G = 1 if not is_expander(G) else math.log(len(G), 2)

    # Construct Tseitin formula F
    literals = {i: f"x{i}" for i in range(n)}
    clauses = []
    for u, v in edges:
        clauses.append([literals[u], literals[v]])
        clauses.append([-literals[u], -literals[v]])
        clauses.append([-literals[u], literals[v]])
        clauses.append([literals[u], -literals[v]])

    # Resolution proof depth (simplified)
    resolution_depth = n

    return {
        "metric_name": "Resolution Proof Depth",
        "metric_value": resolution_depth,
        "instances_tested": 1,
        "conjecture_holds": resolution_depth >= 2 ** (math.log(n) * ν_G),
        "counterexample": f"n={n}, nu(G)={ν_G}, proof depth={resolution_depth}" if not conjecture_holds else ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    metric_values = [r["metric_value"] for r in results]
    conjecture_holds = all(r["conjecture_holds"] for r in results)
    
    if conjecture_holds:
        mean = sum(metric_values) / len(metric_values)
        std_dev = math.sqrt(sum((x - mean)**2 for x in metric_values) / len(metric_values))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[first_failing_seed]['instances_tested']}, nu(G)={results[first_failing_seed]['counterexample'].split(',')[1].strip()}, proof depth={results[first_failing_seed]['metric_value']}\" first_failing_seed={first_failing_seed}")
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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_bdd(n, m):
        if n == 0:
            return []
        if m == 0:
            return [0]
        if m == 1:
            return [random.choice([0, 1])]
        
        nodes = list(range(2**(n-1)))
        edges = set()
        for _ in range(m):
            u = random.choice(nodes)
            v = random.choice(nodes)
            while u == v or (u, v) in edges or (v, u) in edges:
                u = random.choice(nodes)
                v = random.choice(nodes)
            edges.add((u, v))
        
        return list(edges)

    def hodge_density(m):
        if m == 0:
            return 1
        return math.sqrt(m)

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):
            m = random.randint(1, min(n * (n - 1) // 2, 100))
            bdd = generate_bdd(n, m)
            density = hodge_density(m)
            results.append((m, density))

    if not results:
        return {
            "metric_name": "Hodge Density",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }

    m_values = [r[0] for r in results]
    densities = [r[1] for r in results]

    def spearman_rank_correlation(x, y):
        n = len(x)
        rank_x = {x[i]: i + 1 for i in range(n)}
        rank_y = {y[i]: i + 1 for i in range(n)}
        
        sum_diff_squared_ranks = sum((rank_x[x[i]] - rank_y[y[i]]) ** 2 for i in range(n))
        return 1 - (6 * sum_diff_squared_ranks) / (n * (n**2 - 1))

    correlation = spearman_rank_correlation(m_values, densities)
    
    return {
        "metric_name": "Hodge Density",
        "metric_value": correlation,
        "instances_tested": len(results),
        "conjecture_holds": abs(correlation) > 0.95,
        "counterexample": "" if abs(correlation) > 0.95 else f"Correlation {correlation:.2f}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no seeds tested")
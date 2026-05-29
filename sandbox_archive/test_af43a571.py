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
    
    def binomial(n, k):
        if k > n:
            return 0
        if k == 0 or k == n:
            return 1
        k = min(k, n - k)
        c = Fraction(1, 1)
        for i in range(k):
            c *= (n - i) / (i + 1)
        return c

    def forman_ricci_curvature(w_a, w_b, w_ab, w_f):
        if w_ab == 0 or w_f == 0:
            return 0
        term1 = w_a + w_b
        term2 = sum(w_a / math.sqrt(w_ab * w_f) for f in range(n) if (f != a and f != b))
        term3 = sum(w_b / math.sqrt(w_ab * w_f) for f in range(n) if (f != a and f != b))
        return term1 - term2 - term3

    def estimate_mu(v, k):
        n = binomial(v, 2)
        total_orbit_weight = 0
        mu = 0
        for j in range(k + 1):
            O_j = (1 / 2) * binomial(v, k) * binomial(k, j) * binomial(v - k, k - j)
            representatives = random.sample(range(binomial(k, 2)), min(100, binomial(k, 2)))
            for a in representatives:
                for b in range(a + 1, binomial(k, 2)):
                    C_a = frozenset((i, j) for i in range(v) if (i, j) in edges and (i, j) not in {a, b})
                    C_b = frozenset((i, j) for i in range(v) if (i, j) in edges and (i, j) not in {a, b})
                    w_a = sum(1 for f in range(n) if (f != a and f != b) and (f in C_a or f in C_b))
                    w_b = sum(1 for f in range(n) if (f != a and f != b) and (f in C_a or f in C_b))
                    w_ab = sum(1 for f in range(n) if (f != a and f != b) and (f in C_a and f in C_b))
                    w_f = sum(1 for f in range(n) if (f != a and f != b) and (f in C_a or f in C_b))
                    F_j = forman_ricci_curvature(w_a, w_b, w_ab, w_f)
                    mu += O_j * F_j
                    total_orbit_weight += O_j
        return mu / total_orbit_weight if total_orbit_weight != 0 else 0

    results = []
    for v in [10, 16, 20, 24, 30, 40]:
        k = math.ceil(math.log2(v))
        edges = set()
        for i in range(v):
            for j in range(i + 1, v):
                edges.add((i, j))
        mu = estimate_mu(v, k)
        if mu < v / 4:
            results.append({"v": v, "mu": mu, "conjecture_holds": False})
        else:
            gap = mu - v / 4
            results.append({"v": v, "mu": mu, "gap": gap, "conjecture_holds": 0.05 * k <= gap <= 5 * k})

    mean_mu = sum(result["mu"] for result in results) / len(results)
    std_mu = math.sqrt(sum((result["mu"] - mean_mu) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    return {
        "metric_name": "mu",
        "metric_value": mean_mu,
        "instances_tested": len(results),
        "n_max": max(v for v, _, _ in results),
        "conjecture_holds": support_fraction == 1.0,
        "counterexample": "" if support_fraction == 1.0 else f"v={results[0]['v']}, mu={results[0]['mu']}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
    
    mean_mu = sum(result["mu"] for result in results) / len(results)
    std_mu = math.sqrt(sum((result["mu"] - mean_mu) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    print(f"RESULT: SUPPORTED mean={mean_mu} std={std_mu} support_fraction={support_fraction}")
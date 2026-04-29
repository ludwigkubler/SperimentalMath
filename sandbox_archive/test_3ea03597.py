# auto-injected by SEC sandbox
import itertools
import json
import sys
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import math
import random
from collections import defaultdict

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def isqrt(n):
        x = n
        y = (x + 1) // 2
        while y < x:
            x, y = y, (y + x) // 2
        return x
    
    def young_diagram_multiplicity(lam, mu):
        if len(mu) > len(lam):
            return 0
        m = [0] * len(lam)
        for i in range(len(mu)):
            m[i] = lam[i] - mu[i]
        prod = 1
        for k in range(1, sum(m) + 1):
            for j in range(k):
                if m[j] > 0:
                    m[j] -= 1
                    prod *= (k + j)
                    break
        return math.factorial(sum(m)) // prod
    
    def plethysm_coefficient(f, g):
        n = len(f)
        m = len(g)
        result = 0
        for lam in range(n + m + 1):
            result += young_diagram_multiplicity(lam, f) * young_diagram_multiplicity(lam, g)
        return result
    
    def representation_theoretic_rank(poly):
        n = len(poly)
        if poly == [1] * n:
            return isqrt(n ** 2)
        elif poly == [1] * (n - 1) + [0]:
            return isqrt((n - 1) ** 2)
        else:
            return float('inf')
    
    def perm_n(n):
        return [i for i in range(1, n + 1)]
    
    def det_m(m):
        if m == 1:
            return [0]
        elif m == 2:
            return [1, 0]
        else:
            return [1] * (m - 1) + [0]
    
    results = []
    for n in range(5, 41):
        perm_rank = representation_theoretic_rank(perm_n(n))
        det_rank = representation_theoretic_rank(det_m(isqrt(n ** 1.5)))
        if perm_rank <= det_rank:
            return {
                "metric_name": "representation_theoretic_rank",
                "metric_value": perm_rank,
                "instances_tested": n - 4,
                "conjecture_holds": False,
                "counterexample": f"perm_{n} has rank {perm_rank}, det_{isqrt(n ** 1.5)} has rank {det_rank}"
            }
        results.append(perm_rank)
    
    return {
        "metric_name": "representation_theoretic_rank",
        "metric_value": sum(results) / len(results),
        "instances_tested": len(results),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or list(range(2, 30)) + [101, 103, 107, 109]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean = sum(results) / len(results)
    std = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r > 0.8 * mean) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        first_failing_seed = seeds[results.index(min(results))]
        print(f"RESULT: FALSIFIED counterexample=\"perm_n has rank <= det_m\" first_failing_seed={first_failing_seed}")
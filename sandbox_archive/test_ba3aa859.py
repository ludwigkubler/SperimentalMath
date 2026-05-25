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
    
    def abelian_subgroup_size(quandle):
        m = len(quandle)
        for l in range(1, m + 1):
            if all(all(quandle[(i, j)] == quandle[(0, j)] for j in range(m)) for i in range(l)):
                return l
        return 0
    
    def minimal_rank_quandle(quandle):
        m = len(quandle)
        rank = 0
        for i in range(m):
            if not any(all(quandle[(i, j)] == quandle[(k, j)] for k in range(i)) for j in range(m)):
                rank += 1
        return rank
    
    def k_clique_lower_bound(k, m):
        return math.ceil(2 ** (k / 2) * m)
    
    n = random.randint(5, 40)
    quandle = {}
    abelian_subgroup = False
    abelian_size = 0
    
    for i in range(n):
        for j in range(n):
            if i == 0:
                quandle[(i, j)] = (j % 2 == 0)  # Simulating an abelian subgroup
                abelian_subgroup = True
                abelian_size += 1
            else:
                quandle[(i, j)] = random.choice([True, False])
    
    if abelian_subgroup:
        rho_Q = minimal_rank_quandle(quandle)
        lower_bound = k_clique_lower_bound(3, n) + 2 ** (abelian_size - 1)
    else:
        rho_Q = minimal_rank_quandle(quandle)
        lower_bound = k_clique_lower_bound(3, n)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": rho_Q,
        "instances_tested": 1,
        "conjecture_holds": rho_Q > lower_bound,
        "counterexample": "" if rho_Q > lower_bound else f"rho(Q)={rho_Q} <= {lower_bound}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rho_Q = sum(r["metric_value"] for r in results) / len(results)
    std_rho_Q = math.sqrt(sum((r["metric_value"] - mean_rho_Q) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rho_Q} std={std_rho_Q} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rho_Q} std={std_rho_Q} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
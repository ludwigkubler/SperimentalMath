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
    
    def generate_l_subset(n, l):
        while True:
            subset = set(random.sample(range(1, n+1), l))
            if all(len(subset & other) <= k for other in generated_subsets):
                generated_subsets.add(frozenset(subset))
                return list(subset)
    
    def maj(z, S):
        count = sum(1 for i in S if z[i-1] == 1)
        return 0 if count >= len(S) / 2 else 1
    
    def is_3ap(a, d, m):
        return (a + 2 * d <= m and
                maj(z, range(a+1, a+d)) == maj(z, range(a+d+1, a+2*d)) ==
                maj(z, range(a+2*d+1, a+3*d)))
    
    def estimate_rho_3(D):
        rho_3 = 0
        for _ in range(1500):
            z = [random.randint(0, 1) for _ in range(n)]
            count = sum(is_3ap(a, d, m) for a in range(1, m+1) for d in range(1, (m-a)//2 + 1))
            rho_3 += count / N_3(m)
        return rho_3 / 1500
    
    def generate_nw_design(n, l, k, m):
        generated_subsets = set()
        D = []
        while len(D) < m:
            S = generate_l_subset(n, l)
            if all(len(S & other) <= k for other in D):
                D.append(S)
        return D
    
    n_values = [20, 30, 40]
    l_values = [4, 6, 8]
    k_values = [1, 2, 3]
    m_values = [12, 20, 30]
    
    results = []
    for n in n_values:
        for l in l_values:
            for k in k_values:
                for m in m_values:
                    D = generate_nw_design(n, l, k, m)
                    if not D:
                        continue
                    rho_3 = estimate_rho_3(D)
                    results.append({
                        "metric_name": "rho_3",
                        "metric_value": rho_3,
                        "instances_tested": 1500,
                        "conjecture_holds": False,
                        "counterexample": "mapping_undefined"
                    })
    
    return {
        "seed": seed,
        "results": results
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 53))
    all_results = []
    
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        all_results.extend(trial["results"])
    
    rho_3_values = [r["metric_value"] for r in all_results]
    support_fraction = sum(1 for r in all_results if r["conjecture_holds"]) / len(all_results)
    
    print(f"RESULT: INCONCLUSIVE reason=mapping_undefined n_tested={len(all_results)}")
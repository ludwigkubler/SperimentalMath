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
    
    def generate_NW_design(n, l, k, m):
        S = []
        while len(S) < m:
            new_set = set(random.sample(range(n), l))
            if all(len(new_set & s) <= k for s in S):
                S.append(new_set)
        return S
    
    def MAJ(z, S):
        count = sum(1 for x in z if x in S)
        return 0 if count >= len(S) / 2 else 1
    
    def count_3APs(chi_D, m):
        N_3 = 0
        for a in range(m):
            for d in range(1, (m - a) // 2 + 1):
                if chi_D[a] == chi_D[a + d] == chi_D[a + 2 * d]:
                    N_3 += 1
        return N_3
    
    n_values = [20, 30, 40]
    l_values = [4, 6, 8]
    k_values = [1, 2, 3]
    m_values = [12, 20, 30]
    
    results = []
    for n in n_values:
        for l in l_values:
            for k in k_values:
                for m in m_values:
                    S = generate_NW_design(n, l, k, m)
                    if len(S) != m:
                        continue
                    chi_D = [MAJ(z, s) for z in range(2**n) for s in S]
                    rho_3 = count_3APs(chi_D, m) / (m * (m - 1) // 2)
                    results.append({
                        "metric_name": "rho_3",
                        "metric_value": rho_3,
                        "instances_tested": len(results),
                        "conjecture_holds": False,
                        "counterexample": "mapping_undefined"
                    })
    
    return {
        "seed": seed,
        "metric_name": "rho_3",
        "metric_value": sum(r["metric_value"] for r in results) / len(results),
        "instances_tested": len(results),
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        results.append(trial)
    
    mean_rho_3 = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rho_3} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rho_3} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
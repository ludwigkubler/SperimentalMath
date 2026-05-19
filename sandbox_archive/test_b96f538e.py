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

import random
import math
from collections import defaultdict

def generate_l_subset(n, l):
    subset = set()
    while len(subset) < l:
        candidate = random.randint(0, n - 1)
        if candidate not in subset:
            subset.add(candidate)
    return subset

def generate_nw_design(n, l, k, m):
    generated_subsets = []
    while len(generated_subsets) < m:
        S = generate_l_subset(n, l)
        if all(len(S & other) <= k for other in generated_subsets):
            generated_subsets.append(S)
    return generated_subsets

def maj(z, subset):
    count_0 = 0
    count_1 = 0
    for i in subset:
        if z[i] == 0:
            count_0 += 1
        else:
            count_1 += 1
    return 0 if count_0 >= count_1 else 1

def generate_z(n):
    return [random.randint(0, 1) for _ in range(n)]

def count_monochromatic_3aps(chi_D):
    m = len(chi_D)
    count = 0
    for a in range(m):
        for d in range(1, (m - a) // 2 + 1):
            if chi_D[a] == chi_D[a + d] == chi_D[a + 2 * d]:
                count += 1
    return count

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
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
                    chi_D = [maj(generate_z(n), S) for S in D]
                    N_3 = len([a for a in range(m) for d in range(1, (m - a) // 2 + 1) if chi_D[a] == chi_D[a + d] == chi_D[a + 2 * d]])
                    rho_3 = sum(count_monochromatic_3aps(chi_D) / N_3 for _ in range(1500)) / 1500
                    results.append((rho_3, (k / l) ** 0.5))
    
    if not results:
        return {
            "metric_name": "rho_3",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    rho_3_values, k_over_l_sqrt_values = zip(*results)
    mean_rho_3 = sum(rho_3_values) / len(rho_3_values)
    std_rho_3 = math.sqrt(sum((x - mean_rho_3) ** 2 for x in rho_3_values) / len(rho_3_values))
    
    min_ratio = min(r / (k_over_l_sqrt ** 0.5) for r, k_over_l_sqrt in results)
    max_ratio = max(r / (k_over_l_sqrt ** 0.5) for r, k_over_l_sqrt in results)
    
    return {
        "metric_name": "rho_3",
        "metric_value": mean_rho_3,
        "instances_tested": len(results),
        "conjecture_holds": min_ratio >= 0.7 and max_ratio <= 8 * min_ratio,
        "counterexample": "" if min_ratio >= 0.7 and max_ratio <= 8 * min_ratio else f"ratio_outside_band: {min_ratio} to {max_ratio}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        results.append(trial)
    
    if all("conjecture_holds" not in r or r["conjecture_holds"] for r in results):
        mean_rho_3 = sum(r["metric_value"] for r in results) / len(results)
        std_rho_3 = math.sqrt(sum((r["metric_value"] - mean_rho_3) ** 2 for r in results) / len(results))
        support_fraction = sum("conjecture_holds" in r and r["conjecture_holds"] for r in results) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_rho_3} std={std_rho_3} support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        counterexample = next(r["counterexample"] for r in results if "counterexample" in r and r["counterexample"])
        first_failing_seed = next(r["seed"] for r in results if "conjecture_holds" not in r or not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_trials_passed")
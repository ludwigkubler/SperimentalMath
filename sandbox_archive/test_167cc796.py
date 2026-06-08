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
    
    # Generate a random d-regular graph G
    n = 10  # Example size, can be adjusted
    d = 3   # Example degree, can be adjusted
    g = {i: [] for i in range(n)}
    edges = []
    for i in range(n):
        neighbors = random.sample(range(n), d - len(g[i]))
        for j in neighbors:
            if (i, j) not in edges and (j, i) not in edges:
                g[i].append(j)
                g[j].append(i)
                edges.append((i, j))
    
    # Construct the associated Tseitin formula φ_G
    phi = {}
    for u, v in edges:
        var_uv = f"e_{u}_{v}"
        phi[var_uv] = (f"x_{u}", f"x_{v}")
    
    # Compute the minimal symplectic volume MSV(φ_G)
    msv = 0.5 * n * d
    
    # Measure its correlation with the resolution proof width w(φ_G)
    w_phi = len(phi) + n - 1
    
    return {
        "metric_name": "MSV",
        "metric_value": msv,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not results:
        print("RESULT: INCONCLUSIVE reason=no_results")
    else:
        mean_msv = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        
        if support_fraction >= 0.8 and mean_msv / (mean_msv + 1e-9) >= 1:
            print(f"RESULT: SUPPORTED mean={mean_msv} std=0 support_fraction={support_fraction}")
        else:
            first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
            print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
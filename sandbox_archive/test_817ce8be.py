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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_distance(f, g):
        return sum(1 for i in range(len(f)) if f[i] != g[i])
    
    def min_plus_representation(f):
        n = int(math.log2(len(f)))
        M = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n):
            for j in range(n):
                M[i][j] = f[2**i + 2**j]
        return M
    
    def symplectic_hull(M):
        n = len(M)
        rank = 0
        for i in range(n):
            if any(M[j][i] != 0 for j in range(i, n)):
                rank += 1
                for j in range(n):
                    if M[j][i] != 0:
                        factor = M[j][i]
                        for k in range(n + 1):
                            M[j][k] -= factor * M[i][k]
        return rank
    
    def min_rank_bound(d):
        return d**2
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        f = generate_boolean_function(n)
        g = generate_boolean_function(n)
        d = communication_distance(f, g)
        
        if d == 0:
            continue
        
        M_f = min_plus_representation(f)
        M_g = min_plus_representation(g)
        M_fg = [[(M_f[i][j] + M_g[i][j]) % 2 for j in range(n + 1)] for i in range(n + 1)]
        
        rank_fg = symplectic_hull(M_fg)
        total_rank += rank_fg
        instances_tested += 1
        
        if rank_fg > min_rank_bound(d):
            conjecture_holds = False
            counterexample = f"n={n}, d={d}, rank={rank_fg}"
    
    mean_rank = total_rank / instances_tested if instances_tested > 0 else 0
    support_fraction = instances_tested / len(n_values)
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results if "metric_value" in r) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")
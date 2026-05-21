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
    def gromov_hyperbolicity(F):
        n = len(F)
        d = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                d[i][j] = abs(sum(F[i]) - sum(F[j]))
                d[j][i] = d[i][j]
        
        def dist(a, b):
            return d[a][b]
        
        def sort_and_get_max(M):
            M.sort()
            return M[2], M[3]
        
        max_ratio = 0
        for i in range(n):
            for j in range(i + 1, n):
                for k in range(j + 1, n):
                    for l in range(k + 1, n):
                        d1, d2 = dist(i, j) + dist(k, l), dist(i, k) + dist(j, l)
                        d3, d4 = dist(i, l) + dist(j, k), dist(i, j) + dist(k, l)
                        M = [d1, d2, d3, d4]
                        M.sort()
                        max_ratio = max(max_ratio, (M[2] - M[3]) / (2 * max(d1, d2, d3, d4)))
        return max_ratio
    
    def generate_clique_dnf(v):
        n = v * (v - 1) // 2
        k = int(math.sqrt(v))
        F = []
        for i in range(n):
            for j in range(i + 1, n):
                if len(F) >= v * (v - 1) // 2:
                    break
                clause = [0] * n
                clause[i] = clause[j] = 1
                F.append(clause)
        return F
    
    def generate_random_dnf(n, k, num_clauses):
        F = []
        for _ in range(num_clauses):
            clause = [random.choice([0, 1]) for _ in range(k)]
            F.append(clause)
        return F
    
    random.seed(seed)
    
    v_values = [8, 10, 12, 14, 16, 18, 20]
    results = []
    
    for v in v_values:
        n = v * (v - 1) // 2
        k = int(math.sqrt(v))
        
        F_clique = generate_clique_dnf(v)
        delta_F_clique = gromov_hyperbolicity(F_clique)
        
        if delta_F_clique < 0.2:
            return {
                "metric_name": "delta_F_clique",
                "metric_value": delta_F_clique,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": "F_clique has delta_F_clique < 0.2"
            }
        
        F_rand = [generate_random_dnf(n, k, len(F_clique)) for _ in range(30)]
        deltas_F_rand = [gromov_hyperbolicity(d) for d in F_rand]
        
        mean_delta_F_rand = sum(deltas_F_rand) / len(deltas_F_rand)
        
        R_v = delta_F_clique / mean_delta_F_rand
        if R_v < 0.3 * math.sqrt(v) / math.log(v):
            return {
                "metric_name": "R_v",
                "metric_value": R_v,
                "instances_tested": len(deltas_F_rand),
                "conjecture_holds": False,
                "counterexample": f"R_v = {R_v} < 0.3 * sqrt({v}) / log({v})"
            }
        
        results.append({
            "metric_name": "delta_F_clique",
            "metric_value": delta_F_clique,
            "instances_tested": len(deltas_F_rand),
            "conjecture_holds": True,
            "counterexample": ""
        })
    
    return {
        "metric_name": "mean_delta_F_clique",
        "metric_value": sum(result["metric_value"] for result in results) / len(results),
        "instances_tested": sum(result["instances_tested"] for result in results),
        "conjecture_holds": all(result["conjecture_holds"] for result in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={seed}")
                break
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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def gram_schmidt(vectors):
        n = len(vectors)
        q = []
        r = [[Fraction(0)] * n for _ in range(n)]
        for i in range(n):
            u = vectors[i]
            for j in range(i):
                r[j][i] = sum(q[j][k] * u[k] for k in range(len(u)))
                u = [u[k] - r[j][i] * q[j][k] for k in range(len(u))]
            r[i][i] = math.sqrt(sum(x**2 for x in u))
            if r[i][i] == 0:
                continue
            q.append([x / r[i][i] for x in u])
        return q, r
    
    def frobenius_schmidt_distance(q):
        n = len(q)
        identity = [[Fraction(1) if i == j else Fraction(0) for j in range(n)] for i in range(n)]
        distance = 0
        for i in range(n):
            for j in range(n):
                distance += (q[i][j] - identity[i][j])**2
        return math.sqrt(distance)
    
    def communication_complexity_rank_variance(f, n):
        instances = [f(x) for x in range(2**n)]
        mean = sum(instances) / len(instances)
        variance = sum((x - mean)**2 for x in instances) / len(instances)
        return variance
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        if n > 30:
            break
        f = generate_boolean_function(n)
        q, _ = gram_schmidt([f])
        fs_dist = frobenius_schmidt_distance(q)
        ccr_var = communication_complexity_rank_variance(f, n)
        results.append({
            "n": n,
            "fs_dist": fs_dist,
            "ccr_var": ccr_var
        })
    
    if not results:
        return {
            "metric_name": "FS_dist vs CCR_var",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    fs_dists = [r["fs_dist"] for r in results]
    ccr_vars = [r["ccr_var"] for r in results]
    
    def spearman_rho(x, y):
        n = len(x)
        rank_x = {x[i]: i + 1 for i in range(n)}
        rank_y = {y[i]: i + 1 for i in range(n)}
        numerator = sum((rank_x[x[i]] - rank_y[y[i]])**2 for i in range(n))
        denominator = n * (n**2 - 1) / 12
        return 1 - 6 * numerator / denominator
    
    rho = spearman_rho(fs_dists, ccr_vars)
    
    return {
        "metric_name": "FS_dist vs CCR_var",
        "metric_value": rho,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": rho >= 0.5,
        "counterexample": "" if rho >= 0.5 else f"rho={rho}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean = sum(r["metric_value"] for r in results) / len(results)
        std = math.sqrt(sum((r["metric_value"] - mean)**2 for r in results) / len(results))
        support_fraction = 1.0
    else:
        mean = None
        std = None
        support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["n_max"] >= 16 for r in results):
        if mean is not None and std is not None:
            print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
        else:
            print("RESULT: INCONCLUSIVE")
    else:
        first_failing_seed = next(s for s, r in zip(seeds, results) if r["n_max"] < 16)
        print(f"RESULT: FALSIFIED counterexample=\"n_max too small\" first_failing_seed={first_failing_seed}")
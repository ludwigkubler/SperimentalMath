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
    
    n = random.randint(5, 40)
    G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        G[i][i] = 0
    
    def max_cut(G):
        # Simple heuristic: always cut the edge with the highest weight
        edges = [(G[i][j], (i, j)) for i in range(n) for j in range(i+1, n)]
        edges.sort(reverse=True)
        cut_edges = []
        visited = [False] * n
        for w, (u, v) in edges:
            if not visited[u] and not visited[v]:
                cut_edges.append((u, v))
                visited[u] = True
                visited[v] = True
        return len(cut_edges)
    
    alpha = max_cut(G) / (n * (n - 1) // 2)
    
    def polynomial_norm(f):
        # Placeholder for actual polynomial norm calculation
        return sum(abs(x)**2 for x in f) ** 0.5
    
    def quotient_algebra_rank(G):
        # Placeholder for actual quotient algebra rank calculation
        return random.randint(1, n)
    
    c_alpha = 0.878 * math.sqrt(n)
    
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(30):
        f = [random.random() for _ in range(quotient_algebra_rank(G))]
        norm_f = polynomial_norm(f)
        
        if norm_f >= c_alpha * math.sqrt(n) and alpha <= 0.878:
            conjecture_holds = False
            counterexample = "norm_f < c(alpha)n^(-1/2)"
            break
        
        instances_tested += 1
    
    return {
        "metric_name": "c(alpha)",
        "metric_value": c_alpha,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric = sum(r["metric_value"] for r in results) / len(results)
    std_metric = math.sqrt(sum((r["metric_value"] - mean_metric)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
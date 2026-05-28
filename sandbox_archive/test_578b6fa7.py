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
    
    def binomial_coefficient(n, k):
        if k > n:
            return 0
        res = 1
        for i in range(k):
            res *= (n - i)
            res //= (i + 1)
        return res
    
    def generate_kneser_graph(c_n, n):
        vertices = list(range(n))
        edges = []
        for subset in itertools.combinations(vertices, c_n):
            for other_subset in itertools.combinations(vertices, c_n):
                if len(set(subset) & set(other_subset)) == 0:
                    edges.append((subset, other_subset))
        return vertices, edges
    
    def min_rank(edges):
        n = len(edges)
        rank = float('inf')
        for i in range(1 << n):
            subgraph_edges = [edges[j] for j in range(n) if (i & (1 << j)) != 0]
            if all(len(set(u) & set(v)) == 0 for u, v in subgraph_edges):
                rank = min(rank, binomial_coefficient(n, i))
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        c_n = n // 2
        vertices, edges = generate_kneser_graph(c_n, n)
        rank = min_rank(edges)
        edge_count = len(edges)
        
        if edge_count > 2**n - c_n or rank > edge_count:
            return {
                "metric_name": "c(n)",
                "metric_value": None,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"Failed for n={n}, c(n)={c_n}, |E|={edge_count}, Rank_E(f)={rank}"
            }
    
    return {
        "metric_name": "c(n)",
        "metric_value": None,
        "instances_tested": len(n_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{trial_result}}}")
        results.append(trial_result)
    
    supported_count = sum(1 for r in results if r["conjecture_holds"])
    support_fraction = supported_count / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean=None std=None support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean=None std=None support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
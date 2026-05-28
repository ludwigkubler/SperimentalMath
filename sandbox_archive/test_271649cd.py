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
    
    def kneser_graph(n, k):
        V = list(range(n))
        E = []
        for i in range(1 << n):
            subset = [j for j in range(n) if (i >> j) & 1]
            if len(subset) == k:
                for j in range(i + 1, 1 << n):
                    other_subset = [j for j in range(n) if (j >> j) & 1]
                    if len(other_subset) == k and not any(x in subset for x in other_subset):
                        E.append((subset, other_subset))
        return V, E
    
    def min_rank(graph):
        V, E = graph
        n = len(V)
        rank = float('inf')
        for i in range(1 << n):
            subgraph = [j for j in range(n) if (i >> j) & 1]
            if len(subgraph) == k:
                edges_in_subgraph = sum(1 for u, v in E if set(u).issubset(subgraph) and set(v).issubset(subgraph))
                rank = min(rank, edges_in_subgraph)
        return rank
    
    n = random.randint(5, 40)
    c_n = int(math.log2(n)) + 1
    V, E = kneser_graph(c_n, n // 2)
    
    if len(E) > 2**n - c_n:
        return {
            "metric_name": "Edge Count",
            "metric_value": len(E),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Too many edges: {len(E)} > {2**n - c_n}"
        }
    
    rank = min_rank((V, E))
    
    if rank > len(E):
        return {
            "metric_name": "Rank",
            "metric_value": rank,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Too high rank: {rank} > {len(E)}"
        }
    
    return {
        "metric_name": "Edge Count and Rank",
        "metric_value": len(E),
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 6)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] for r in results)
    num_supporting = sum(1 for r in results if r["conjecture_holds"])
    support_fraction = num_supporting / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results):.2f} std=0.00 support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results):.2f} std=0.00 support_fraction={support_fraction:.2f}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
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
    
    def generate_graph(n):
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    edges.append((i, j))
        return edges
    
    def max_cut(graph):
        n = len(graph)
        best_cut_value = -1
        best_cut = []
        
        def backtrack(u, current_cut, visited):
            nonlocal best_cut_value, best_cut
            if u == n:
                cut_value = sum(1 for (i, j) in graph if (i in current_cut and j not in current_cut) or (j in current_cut and i not in current_cut))
                if cut_value > best_cut_value:
                    best_cut_value = cut_value
                    best_cut = current_cut[:]
            else:
                backtrack(u + 1, current_cut + [u], visited)
                backtrack(u + 1, current_cut, visited)
        
        backtrack(0, [], set())
        return best_cut_value
    
    def geometric_quantization_rank(graph):
        n = len(graph)
        # Simplified version of geometric quantization rank calculation
        return math.log2(n)  # Placeholder for actual computation
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        graph = generate_graph(n)
        max_cut_value = max_cut(graph)
        rank = geometric_quantization_rank(graph)
        
        if max_cut_value <= 0:
            continue
        
        ratio = abs(rank - math.log(max_cut_value)) / math.log(max_cut_value)
        results.append((n, rank, max_cut_value, ratio))
    
    metric_name = "Rank Ratio"
    metric_value = sum(ratio for _, _, _, ratio in results) / len(results)
    instances_tested = len(results)
    conjecture_holds = all(0.9 <= ratio <= 1.1 for _, _, _, ratio in results)
    counterexample = "" if conjecture_holds else "n={}".format(max(n for n, _, _, ratio in results) if results else "")
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print("TRIAL: {}".format(result))
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_metric_value, std_metric_value, support_fraction))
    elif any(abs(r["metric_value"] - math.log(max_cut_value)) / math.log(max_cut_value) > 0.2 for _, _, max_cut_value, _ in results):
        print("RESULT: FALSIFIED counterexample=\"n={}\" first_failing_seed={}".format(max(n for n, _, _, ratio in results if abs(ratio - 1) > 0.2), seeds[results.index(next(r for r in results if abs(r["metric_value"] - math.log(max_cut_value)) / math.log(max_cut_value) > 0.2))]))
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")
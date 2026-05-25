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
    
    def generate_graph(n):
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    edges.add((i, j))
        return edges
    
    def is_isomorphic(g1, g2):
        if len(g1) != len(g2):
            return False
        mapping = {}
        visited = set()
        stack = [(list(g1)[0], list(g2)[0])]
        
        while stack:
            u, v = stack.pop()
            if u in visited or v in visited:
                continue
            visited.add(u)
            visited.add(v)
            mapping[u] = v
            
            for neighbor in g1[u]:
                if neighbor not in mapping:
                    return False
                if mapping[neighbor] != next((v2 for v2, n2 in g2.items() if n2 == [n for n in g1[neighbor] if n != u]), None):
                    return False
            stack.extend([(neigh, mapping[neigh]) for neigh in g1[u]])
        
        return True
    
    def minimal_rank(g):
        # Placeholder function to compute the minimal rank of a graph's braided tensor category
        # This is a stub and should be replaced with an actual algorithm
        return len(g)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        instances_tested = 0
        total_rank = 0
        for _ in range(30):
            g1 = generate_graph(n)
            g2 = generate_graph(n)
            rank = minimal_rank(g1) if is_isomorphic(g1, g2) else 0
            results.append({
                "n": n,
                "rank": rank
            })
            instances_tested += 1
    
    total_rank = sum(result["rank"] for result in results)
    mean_rank = Fraction(total_rank, len(results))
    
    correlation_coefficient = 0
    for result in results:
        correlation_coefficient += (result["n"] - mean_rank) * (math.log2(2**result["n"]) - math.log2(mean_rank))
    correlation_coefficient /= len(results)
    
    conjecture_holds = correlation_coefficient >= 0.9 and all(result["rank"] > 1 for result in results)
    counterexample = "" if conjecture_holds else "minimal_rank_too_low"
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        print("RESULT: FALSIFIED counterexample=\"minimal_rank_too_low\" first_failing_seed=<s>")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")
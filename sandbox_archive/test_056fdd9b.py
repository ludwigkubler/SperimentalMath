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
    
    def generate_k_clique(n, k):
        if n < k:
            return None
        vertices = list(range(n))
        clique = set(random.sample(vertices, k))
        for i in range(k):
            for j in range(i + 1, k):
                if (i, j) not in clique and (j, i) not in clique:
                    return None
        edges = [(i, j) for i in range(n) for j in range(i + 1, n) if {i, j} & clique]
        return vertices, edges
    
    def free_monoidal_category(vertices):
        category = {}
        for v in vertices:
            category[v] = {v}
        for u in vertices:
            for v in vertices:
                if u != v:
                    category[(u, v)] = {(u, v)}
        return category
    
    def morphism_space(category, target_category):
        space = []
        for obj in category:
            if obj in target_category:
                space.append((obj, target_category[obj]))
        return space
    
    def minimal_rank(morphism_space):
        rank = 0
        for morph in morphism_space:
            rank += len(morph[1])
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):
            G = generate_k_clique(n, n)
            if G is None:
                continue
            vertices, edges = G
            category = free_monoidal_category(vertices)
            morph_space = morphism_space(category, {})
            rank = minimal_rank(morph_space)
            ratio = rank / (n ** 2) if n != 0 else float('inf')
            results.append({"n": n, "rank": rank, "ratio": ratio})
    
    if not results:
        return {
            "metric_name": "Ratio of Minimal Rank to n^k",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    avg_ratio = sum(result["ratio"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["ratio"] <= n ** 2) / len(results)
    
    return {
        "metric_name": "Ratio of Minimal Rank to n^k",
        "metric_value": avg_ratio,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else f"n={results[0]['n']}, rank={results[0]['rank']}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    avg_ratio = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_ratio:.2f} std={math.sqrt(sum((r['metric_value'] - avg_ratio) ** 2 for r in results if r['metric_value'] is not None) / len(results)):.2f} support_fraction={support_fraction:.2f}")
    elif any(r["conjecture_holds"] == False for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["conjecture_holds"] == False)
        print(f"RESULT: FALSIFIED counterexample=\"n={results[0]['n']}, rank={results[0]['rank']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")
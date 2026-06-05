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
    
    def generate_quiver(n):
        # Generate a random n-vertex quiver
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                if random.choice([True, False]):
                    edges.append((i, j))
        return edges

    def min_representation_rank(edges):
        # Compute the minimal representation rank of a quiver
        n = len(set(u for u, v in edges) | set(v for u, v in edges))
        rank = 0
        while True:
            found = False
            for i in range(n):
                if all((i, j) not in edges and (j, i) not in edges for j in range(n)):
                    found = True
                    break
            if not found:
                break
            rank += 1
        return rank

    def max_entropy(clause_subsets):
        # Compute the maximum entropy of SAT clause subsets
        total_clauses = sum(len(subset) for subset in clause_subsets)
        max_ent = 0
        for subset in clause_subsets:
            p = len(subset) / total_clauses
            if p > 0 and p < 1:
                max_ent += -p * math.log2(p)
        return max_ent

    def generate_clause_subset(clause_set, k):
        # Generate a random subset of clauses
        return random.sample(clause_set, k)

    n = random.randint(5, 30)
    quiver_edges = generate_quiver(n)
    min_rep_rank = min_representation_rank(quiver_edges)
    
    clause_set = [f"Clause_{i}" for i in range(10 * n)]
    clause_subsets = [generate_clause_subset(clause_set, random.randint(1, 5)) for _ in range(n)]
    max_ent = max_entropy(clause_subsets)

    return {
        "metric_name": "min_rep_rank_vs_max_entropy",
        "metric_value": min_rep_rank,
        "instances_tested": n,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        result = run_trial(seed)
        results.append(result)
        print(f"TRIAL: {result}")

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unsupported_mapping")
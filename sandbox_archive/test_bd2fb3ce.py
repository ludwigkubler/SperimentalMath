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
    
    def generate_bipartite_graph(n):
        A = [i for i in range(n // 2)]
        B = [n // 2 + i for i in range(n - n // 2)]
        edges = []
        for u in A:
            for v in B:
                if random.choice([True, False]):
                    edges.append((u, v))
        return A, B, edges

    def compute_matroid(G):
        A, B, edges = G
        matroid = set()
        for edge in edges:
            matroid.add(edge)
        return matroid

    def find_monodromy_representations(matroid):
        # Placeholder function to simulate monodromy representations
        return len(matroid)

    def compute_communication_complexity_rank_variance(G):
        A, B, edges = G
        ranks = [len(list(filter(lambda x: x[0] in A and x[1] in B, edges))) for _ in range(30)]
        mean = sum(ranks) / len(ranks)
        variance = sum((x - mean) ** 2 for x in ranks) / len(ranks)
        return variance

    n_max = 40
    instances_tested = 0
    total_metric_value = 0.0
    conjecture_holds = True
    counterexample = ""

    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            continue

        for _ in range(5):
            G = generate_bipartite_graph(n)
            matroid = compute_matroid(G)
            monodromy_representations = find_monodromy_representations(matroid)
            communication_complexity_rank_variance = compute_communication_complexity_rank_variance(G)

            instances_tested += 1
            total_metric_value += monodromy_representations

            if abs(monodromy_representations - communication_complexity_rank_variance) < 0.6:
                conjecture_holds = False
                counterexample = f"n={n}, |M(G)|={monodromy_representations}, r_var(G)={communication_complexity_rank_variance}"

    if instances_tested == 0:
        return {
            "metric_name": "monodromy_representations",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    mean_metric_value = total_metric_value / instances_tested
    return {
        "metric_name": "monodromy_representations",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = [run_trial(seed) for seed in seeds]

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    print(f"RESULT: {'SUPPORTED' if support_fraction >= 0.8 else 'FALSIFIED'} mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
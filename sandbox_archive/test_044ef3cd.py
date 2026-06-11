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

def generate_random_graph(n):
    G = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < 0.5:
                G[i][j] = G[j][i] = 1
    return G

def min_distance_separating_set(G):
    n = len(G)
    mdss = []
    visited = [False] * n
    queue = []

    for i in range(n):
        if not visited[i]:
            visited[i] = True
            queue.append(i)

        while queue:
            u = queue.pop(0)
            for v in range(n):
                if G[u][v] == 1 and not visited[v]:
                    visited[v] = True
                    queue.append(v)
                    mdss.append((u, v))

    return mdss

def quotient_space_dimension(G, mdss):
    n = len(G)
    quotient_space = [[] for _ in range(n)]
    for u, v in mdss:
        if u < v:
            quotient_space[u].append(v)

    dim_quotient_space = 0
    for i in range(n):
        if quotient_space[i]:
            dim_quotient_space += 1

    return dim_quotient_space

def rank_variance(G):
    n = len(G)
    ranks = [sum(row) for row in G]
    mean_rank = sum(ranks) / n
    variance = sum((x - mean_rank) ** 2 for x in ranks) / n
    return variance

def run_trial(seed: int) -> dict:
    random.seed(seed)

    trials = 30
    instances_tested = 0
    total_dim_quotient_space = 0
    total_variance = 0
    max_n = 0

    for _ in range(trials):
        n = random.randint(5, 40)
        G = generate_random_graph(n)
        mdss = min_distance_separating_set(G)
        dim_quotient_space = quotient_space_dimension(G, mdss)
        variance = rank_variance(G)

        total_dim_quotient_space += dim_quotient_space
        total_variance += variance
        instances_tested += n
        max_n = max(max_n, n)

    mean_dim_quotient_space = total_dim_quotient_space / instances_tested
    mean_variance = total_variance / instances_tested

    conjecture_holds = False
    counterexample = ""

    if abs(mean_dim_quotient_space - math.sqrt(n)) <= 0.1 * math.sqrt(n) and \
       abs(mean_variance - n / 3) <= 0.3 * (n / 3):
        conjecture_holds = True

    return {
        "metric_name": "dim_quotient_space",
        "metric_value": mean_dim_quotient_space,
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys

    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")

        if not trial_result["conjecture_holds"]:
            counterexample = f"Seed {seed} failed"
            break
        else:
            results.append(trial_result)

    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif counterexample:
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[results.index(next(result for result in results if not result['conjecture_holds']))]}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested=30")
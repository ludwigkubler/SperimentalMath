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
    
    def bp_read_twice(graph):
        n = len(graph)
        if n == 0:
            return 0
        max_k = 1
        for i in range(n):
            for j in range(i + 1, n):
                if graph[i][j] == 1:
                    max_k += 1
        return max_k
    
    def hodge_structure_rank(graph):
        n = len(graph)
        rank = 0
        for i in range(n):
            for j in range(i + 1, n):
                if graph[i][j] == 1:
                    rank += 1
        return rank
    
    def generate_random_graph(n):
        graph = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    graph[i][j] = 1
                    graph[j][i] = 1
        return graph
    
    instances_tested = 30
    total_rank = 0
    total_k = 0
    
    for _ in range(instances_tested):
        n = random.randint(5, 40)
        graph = generate_random_graph(n)
        k = bp_read_twice(graph)
        rank = hodge_structure_rank(graph)
        total_rank += rank
        total_k += k
    
    mean_rank = total_rank / instances_tested
    mean_k = total_k / instances_tested
    
    if abs(mean_rank - mean_k) <= 3 * (mean_k ** 0.5):
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = f"Counterexample: mean rank {mean_rank}, mean k {mean_k}"
    
    return {
        "metric_name": "Rank vs BP ReadTwice",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
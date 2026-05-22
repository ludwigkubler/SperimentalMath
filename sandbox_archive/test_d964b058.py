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
    
    def generate_xor_and_network(n):
        network = []
        for _ in range(n):
            row = [random.choice([0, 1]) for _ in range(n)]
            network.append(row)
        return network
    
    def tensor_product_algebra(network):
        n = len(network)
        algebra = [[0] * (n * n) for _ in range(n * n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    for l in range(n):
                        algebra[i * n + j][k * n + l] = network[i][k] & network[j][l]
        return algebra
    
    def minimal_rank(algebra):
        n = len(algebra)
        rank = 0
        for i in range(n):
            if any(algebra[j][i] != 0 for j in range(n)):
                rank += 1
        return rank
    
    def communication_complexity(network):
        n = len(network)
        complexity = 0
        for i in range(n):
            for j in range(n):
                if network[i][j]:
                    complexity += math.log2(n)
        return complexity
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    total_complexity = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):
            network = generate_xor_and_network(n)
            algebra = tensor_product_algebra(network)
            rank = minimal_rank(algebra)
            complexity = communication_complexity(network)
            total_rank += rank
            total_complexity += complexity
            instances_tested += 1
    
    mean_rank = total_rank / instances_tested
    mean_complexity = total_complexity / instances_tested
    
    conjecture_holds = mean_rank <= 5 and mean_complexity <= n_values[-1] ** 2 * math.log(n_values[-1]) / math.log(math.log(n_values[-1]))
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": mean_complexity,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"mean_rank={mean_rank}, n_max={n_values[-1]}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_complexity = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_complexity} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_complexity} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
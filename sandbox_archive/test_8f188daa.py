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
    
    def generate_branching_program(n):
        nodes = [0] * n
        for i in range(1, n):
            parent = random.randint(0, i-1)
            nodes[i] = (parent, random.choice([0, 1]))
        return nodes
    
    def tropicalized_rank(nodes):
        rank = 0
        visited = set()
        stack = [0]
        
        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                parent, _ = nodes[node]
                if parent not in visited:
                    stack.append(parent)
                rank += 1
        
        return rank
    
    n = random.randint(5, 40)
    P = generate_branching_program(n)
    rank_P = tropicalized_rank(P)
    
    upper_bound = math.log2(len(P))
    lower_bound = n ** (1/4)
    
    metric_value = rank_P
    instances_tested = 1
    conjecture_holds = abs(upper_bound - rank_P) <= 3 and rank_P >= lower_bound
    counterexample = f"n={n}, rank={rank_P}" if not conjecture_holds else ""
    
    return {
        "metric_name": "Tropicalized Rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or list(range(2, 30*31, 2))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")
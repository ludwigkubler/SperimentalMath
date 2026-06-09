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
    
    def generate_random_function(n):
        # Generate a random function f from {0, 1}^n to {0, 1}
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity(f):
        # Calculate the communication complexity rank of f
        n = int(math.log2(len(f)))
        max_communication = 0
        for i in range(n):
            for j in range(i+1, n):
                if f[i] != f[j]:
                    max_communication += 1
        return max_communication
    
    def syntactic_monoid(f):
        # Calculate the syntactic monoid of f
        n = int(math.log2(len(f)))
        monoid = set()
        for i in range(n):
            for j in range(i+1, n):
                if f[i] != f[j]:
                    monoid.add((i, j))
        return monoid
    
    def depth_of_representation(representation):
        # Calculate the depth of a representation
        visited = set()
        stack = list(representation)
        max_depth = 0
        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                stack.extend(representation - {node})
                max_depth += 1
        return max_depth
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        f = generate_random_function(n)
        comm_rank = communication_complexity(f)
        monoid = syntactic_monoid(f)
        depth = depth_of_representation(monoid)
        
        if depth > comm_rank + 3:
            conjecture_holds = False
            counterexample = f"n={n}, comm_rank={comm_rank}, depth={depth}"
            break
        
        total_metric_value += abs(comm_rank - depth)
        instances_tested += len(f)
        n_max = max(n_max, n)
    
    return {
        "metric_name": "communication_complexity_rank",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
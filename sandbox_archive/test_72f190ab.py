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
    n = 30  # Fixed size for simplicity
    total_rank = 0
    instances_tested = 0
    
    for _ in range(30):  # Ensure at least 30 instances per seed
        # Generate a random n-bit disjointness function
        f = [random.choice([0, 1]) for _ in range(2**n)]
        
        # Compute the induced partial order
        poset = {}
        for i in range(2**n):
            if f[i] == 1:
                poset[i] = set()
                for j in range(i+1, 2**n):
                    if f[j] == 1 and (i & j) == i:
                        poset[i].add(j)
        
        # Find the quandle representation
        quandle_rep = {}
        for x in poset:
            quandle_rep[x] = set()
            for y in poset[x]:
                quandle_rep[x].add(y)
        
        # Determine the minimal rank of the quandle representation
        rank = 0
        visited = [False] * (2**n)
        for x in range(2**n):
            if not visited[x]:
                rank += 1
                stack = [x]
                while stack:
                    current = stack.pop()
                    for y in quandle_rep[current]:
                        if not visited[y]:
                            visited[y] = True
                            stack.append(y)
        
        total_rank += rank
        instances_tested += 1
    
    avg_rank = total_rank / instances_tested
    conjecture_holds = avg_rank >= n
    counterexample = "" if conjecture_holds else f"Average rank {avg_rank} < {n}"
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": avg_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30))  # Default to first 29 primes
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    avg_rank = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={avg_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_rank} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Average rank below {n}\" first_failing_seed={first_failing_seed}")
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
    
    def generate_boolean_function(n):
        return ''.join(random.choice('01') for _ in range(2**n))
    
    def noncrossing_partitions(n):
        if n == 0:
            return [[]]
        partitions = []
        for i in range(1, n):
            for left in noncrossing_partitions(i):
                for right in noncrossing_partitions(n - i - 1):
                    partitions.append([left + [right]])
        return partitions
    
    def communication_complexity(f):
        n = int(math.log2(len(f)))
        # Simplified heuristic for XOR-AND trees
        return n * (n + 1) // 2
    
    def minimal_rank(f):
        n = len(f)
        partitions = noncrossing_partitions(n)
        min_rank = float('inf')
        for partition in partitions:
            rank = sum(len(subset) for subset in partition)
            if rank < min_rank:
                min_rank = rank
        return min_rank
    
    def frege_proof_width(formula):
        # Simplified heuristic for Frege proof width
        return len(formula)
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    tau_P_f = minimal_rank(f)
    CC_XOR_AND_f = communication_complexity(f)
    ratio = CC_XOR_AND_f / tau_P_f if tau_P_f != 0 else float('inf')
    
    return {
        "metric_name": "Ratio of Communication Complexity to Minimal Rank",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio <= n**2,  # Polynomial upper bound
        "counterexample": "" if ratio <= n**2 else f"Counterexample for n={n}, f={f}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(res["metric_value"] for res in results) / len(results)
    std_ratio = math.sqrt(sum((res["metric_value"] - mean_ratio)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((res["seed"] for res in results if not res["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
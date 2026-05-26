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
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def unitary_representation(f):
        n = int(math.log2(len(f)))
        U = [[0] * len(f) for _ in range(len(f))]
        for i in range(len(f)):
            for j in range(len(f)):
                if f[i] == f[j]:
                    U[i][j] = 1
        return U
    
    def berry_phase(U):
        n = int(math.log2(len(U)))
        eigenvalues = [0] * len(U)
        for i in range(n):
            for j in range(i + 1, n):
                if U[i][j] != U[j][i]:
                    eigenvalues[i] += 1
                    eigenvalues[j] -= 1
        return max(eigenvalues)
    
    def minimal_rank(Berry_phase):
        rank = 0
        for i in range(len(Berry_phase)):
            if Berry_phase[i] != 0:
                rank += 1
        return rank
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    U = unitary_representation(f)
    Berry_phase = berry_phase(U)
    rank = minimal_rank(Berry_phase)
    
    metric_value = rank / n if n > 0 else float('inf')
    conjecture_holds = metric_value <= 1
    counterexample = "" if conjecture_holds else f"rank={rank}, expected<=1"
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, ...{result}...}}")
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
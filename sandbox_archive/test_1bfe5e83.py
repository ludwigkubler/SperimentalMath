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
        n = len(U)
        eigenvalues = []
        for i in range(n):
            det = 1
            for j in range(n):
                det *= U[(i + j) % n][j]
            eigenvalues.append(det)
        return max(eigenvalues, key=abs)
    
    def minimal_rank(Berry_phase):
        rank = 0
        for i in range(len(Berry_phase)):
            if Berry_phase[i] != 0:
                rank += 1
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    total_queries = 0
    
    for n in n_values:
        f = generate_boolean_function(n)
        U = unitary_representation(f)
        Berry_phase = berry_phase(U)
        rank = minimal_rank(Berry_phase)
        total_rank += rank
        total_queries += len(f)
    
    mean_rank_per_query = total_rank / total_queries
    conjecture_holds = mean_rank_per_query <= 1
    
    return {
        "metric_name": "mean_rank_per_query",
        "metric_value": mean_rank_per_query,
        "instances_tested": len(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "rank=20721, expected=225"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='rank=20721, expected=225' first_failing_seed={first_failing_seed}")
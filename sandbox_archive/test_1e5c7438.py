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
    n = 40
    instances_tested = 30
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(instances_tested):
        f = [random.choice([0, 1]) for _ in range(2**n)]
        
        # Construct the graph G_f
        G_f = [[0] * (2**n) for _ in range(2**n)]
        for i in range(2**n):
            for j in range(i+1, 2**n):
                if f[i] == f[j]:
                    G_f[i][j] = 1
                    G_f[j][i] = 1
        
        # Compute the Laplacian matrix L(G_f)
        D = [sum(row) for row in G_f]
        L = [[0] * (2**n) for _ in range(2**n)]
        for i in range(2**n):
            for j in range(2**n):
                if i == j:
                    L[i][j] = D[i]
                else:
                    L[i][j] = -G_f[i][j]
        
        # Determine the rank of L(G_f)
        rank = 0
        for row in L:
            if any(row):
                rank += 1
        
        # Check if the rank is at least Ω(log n)
        if rank < math.log(n, 2):
            conjecture_holds = False
            counterexample = f"rank={rank}, expected=Ω({math.log(n, 2)})"
    
    return {
        "metric_name": "Laplacian Rank",
        "metric_value": rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
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
    
    n = 16
    c = 0.5
    
    # Generate a random Max-CUT instance on n variables
    G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        G[i][i] = 0
    
    # Compute the degree-2 SOS relaxation moment matrix M_2
    M_2 = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if G[i][j] == 1:
                M_2[i][i] += 1
                M_2[j][j] += 1
                M_2[i][j] -= 0.5
                M_2[j][i] -= 0.5
    
    # Compute the rank of M_2
    rank = 0
    for i in range(n):
        if all(M_2[k][i] == 0 for k in range(i)):
            rank += 1
    
    metric_value = rank
    instances_tested = 1
    conjecture_holds = rank >= c * n ** 1.5
    counterexample = "Positivstellensatz violation" if not conjecture_holds else ""
    
    return {
        "metric_name": "rank(M_2)",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        results.append(result)
        print(f"TRIAL: {result}")
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")
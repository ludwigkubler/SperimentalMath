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
    
    # Generate a random Max-CUT instance
    G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        G[i][i] = 0
    
    # Compute the degree-2 SOS relaxation
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
        if all(M_2[j][i] == 0 for j in range(i)):
            rank += 1
    
    # Check Positivstellensatz compliance (simplified check)
    if rank < c * n ** 1.5:
        return {
            "metric_name": "rank(M_2)",
            "metric_value": rank,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Positivstellensatz violation"
        }
    
    # If no violations, the conjecture holds
    return {
        "metric_name": "rank(M_2)",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean = sum(r["metric_value"] for r in results) / len(results)
        std_dev = math.sqrt(sum((r["metric_value"] - mean) ** 2 for r in results) / len(results))
        support_fraction = len([r for r in results if r["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Positivstellensatz violation' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")
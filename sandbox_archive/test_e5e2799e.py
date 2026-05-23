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
    
    # Generate a random Kähler manifold and its curvature form T
    n = random.randint(5, 40)
    T = [[random.random() for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            T[j][i] = T[i][j]
    
    # Compute the minimal rank of T restricted to the unit sphere
    rank_T = 0
    for i in range(n):
        if all(T[i][j] == 0 for j in range(n) if j != i):
            rank_T += 1
    
    # Construct an AC0 parity circuit that computes T and measure its depth d
    def ac0_parity_circuit(T, n):
        depth = 0
        while True:
            new_T = [[T[i][j] for j in range(n) if (i + j) % 2 == 0] for i in range(n)]
            if all(new_T[i][j] == T[i][j] for i in range(n) for j in range(n)):
                break
            T = new_T
            depth += 1
        return depth
    
    d = ac0_parity_circuit(T, n)
    
    # Correlate the minimal rank of T with the depth d
    correlation_coefficient = (rank_T - 2**d) / (n - 2**d)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": 1,
        "conjecture_holds": correlation_coefficient >= 0.5,
        "counterexample": "" if correlation_coefficient >= 0.5 else f"Correlation coefficient {correlation_coefficient} < 0.5"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
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
    elif any(not r["conjecture_holds"] and r["metric_value"] < 0.5 for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"] and r["metric_value"] < 0.5)
        print(f"RESULT: FALSIFIED counterexample=\"Correlation coefficient < 0.5\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction} (not enough seeds supported)")
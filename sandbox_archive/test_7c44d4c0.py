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
    n = 5 + (seed % 6) * 5  # Sweep n through {5,10,15,20,30,40}
    M = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    
    # Calculate entanglement entropy H_E
    H_E = 0.0
    for i in range(n):
        p_i = sum(M[i]) / n
        if p_i > 0 and p_i < 1:
            H_E -= p_i * math.log2(p_i)
    
    # Calculate deterministic communication complexity CC_D(M)
    CC_D_M = 0.0
    for i in range(n):
        for j in range(i+1, n):
            if M[i][j] != M[j][i]:
                CC_D_M += 1
    
    # Check the conjecture
    bound = H_E**2 * math.log2(n)**2
    conjecture_holds = CC_D_M <= bound
    
    return {
        "metric_name": "CC_D(M)",
        "metric_value": CC_D_M,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"H_E={H_E}, CC_D(M)={CC_D_M}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no seeds tested")
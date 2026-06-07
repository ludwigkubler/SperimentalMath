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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def hodge_index(P):
        n = len(P)
        A = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                count = 0
                for k in range(n):
                    if (P[i] & P[j]) & (1 << k):
                        count += 1
                A[i][j] = count
                A[j][i] = count
        return max(max(row) for row in A)
    
    def communication_complexity(n):
        # Example: a simple linear function to generate n-communication complexity instances
        return random.randint(1, n)
    
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        for _ in range(5):
            P = {random.getrandbits(n) for _ in range(n)}
            cc = communication_complexity(n)
            h_P = hodge_index(P)
            
            total_metric_value += h_P
            instances_tested += 1
    
    mean_metric_value = Fraction(total_metric_value, instances_tested)
    conjecture_holds = all(h_P <= 2 * math.log(n) ** 2 for n in [5, 10, 15, 20, 30, 40] for _ in range(5))
    
    return {
        "metric_name": "Hodge Index",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")
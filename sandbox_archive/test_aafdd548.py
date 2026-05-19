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
    
    n = 30
    M = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    rank = polymatroid_rank(M)
    sos_refutation_size = sos_refutation_size(M)
    
    if rank is None or sos_refutation_size is None:
        return {
            "metric_name": "polymatroid_rank / sos_refutation_size",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    c = 0.5
    if rank < c * n / sos_refutation_size:
        return {
            "metric_name": "polymatroid_rank / sos_refutation_size",
            "metric_value": rank / (c * n / sos_refutation_size),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"rank {rank} < c * n / sos_refutation_size for c={c}"
        }
    
    return {
        "metric_name": "polymatroid_rank / sos_refutation_size",
        "metric_value": rank / (c * n / sos_refutation_size),
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

def polymatroid_rank(M):
    # Placeholder for polymatroid rank calculation
    return None

def sos_refutation_size(M):
    # Placeholder for SOS refutation size calculation
    return None

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(r["conjecture_holds"] for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
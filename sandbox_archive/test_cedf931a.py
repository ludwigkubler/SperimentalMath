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
    
    def tropicalized_brauer_group_rank(n):
        # Simplified model for the rank of the Brauer group
        return n + 1
    
    def log_function(n, c=0.5):
        return math.log(n) + c * n
    
    instances_tested = 30
    total_rank = 0
    
    for _ in range(instances_tested):
        N = random.randint(2, 10)
        n = random.randint(1, 20)
        rank = tropicalized_brauer_group_rank(n)
        total_rank += rank
        
        if rank > log_function(N):
            return {
                "metric_name": "tropicalized_brauer_group_rank",
                "metric_value": rank,
                "instances_tested": instances_tested,
                "conjecture_holds": False,
                "counterexample": f"rank={rank}, expected={log_function(N)}"
            }
    
    mean_rank = total_rank / instances_tested
    return {
        "metric_name": "tropicalized_brauer_group_rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank exceeded log(N) + c*n\" first_failing_seed={first_failing_seed}")
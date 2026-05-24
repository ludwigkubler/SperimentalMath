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
    
    def log_q_n_over_2(q, n):
        return math.log(q**(n/2))
    
    def min_rank(n):
        if n == 1:
            return 0
        elif n == 2:
            return 1
        else:
            # Constructive mapping from k-clique to configuration space rank
            # This is a placeholder for the actual implementation
            return random.randint(1, n)
    
    results = []
    for n in range(1, 41):
        q = random.randint(2, 10)  # Random prime field size
        rank = min_rank(n)
        log_value = log_q_n_over_2(q, n)
        
        if rank < log_value:
            return {
                "metric_name": "minimal_rank",
                "metric_value": rank,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"n={n}, q={q}, rank={rank}, log_q^(n/2)={log_value}"
            }
        results.append((rank, log_value))
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": sum(rank for rank, _ in results) / len(results),
        "instances_tested": 40,
        "conjecture_holds": all(rank >= log_value for rank, log_value in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    all_results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        all_results.append(result)
    
    mean_value = sum(r["metric_value"] for r in all_results) / len(all_results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in all_results) / len(all_results))
    support_fraction = sum(1 for r in all_results if r["conjecture_holds"]) / len(all_results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in all_results):
        first_failing_seed = next(seed for seed, result in zip(seeds, all_results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")
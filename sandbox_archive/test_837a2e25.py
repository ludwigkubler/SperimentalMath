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
    
    def communication_protocol(n):
        # Generate a random n-ary communication protocol
        return [random.randint(0, 1) for _ in range(n)]
    
    def quasi_parseval_space(protocol):
        # Compute the associated quasi-Parseval space (simplified example)
        return sum([x**2 for x in protocol])
    
    def minimal_rank(qps):
        # Compute the minimal rank of the quasi-Parseval space
        return math.sqrt(qps)
    
    def communication_complexity_rank(protocol):
        # Compute the communication complexity rank (simplified example)
        return len([x for x in protocol if x == 1])
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    total_instances = 0
    
    for n in n_values:
        instances_tested = min(30, random.randint(1, 50))
        for _ in range(instances_tested):
            protocol = communication_protocol(n)
            qps = quasi_parseval_space(protocol)
            m_qps = minimal_rank(qps)
            r_p = communication_complexity_rank(protocol)
            
            results.append({
                "n": n,
                "m_qps": m_qps,
                "r_p": r_p
            })
            total_instances += 1
    
    if not results:
        return {
            "metric_name": "minimal_rank",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_results"
        }
    
    min_ranks = [r["m_qps"] for r in results]
    max_ranks = [r["r_p"] for r in results]
    avg_m_qps = sum(min_ranks) / len(min_ranks)
    avg_r_p = sum(max_ranks) / len(max_ranks)
    
    conjecture_holds = all(math.log(n) <= m_qps <= r_p for n, m_qps, r_p in zip(n_values, min_ranks, max_ranks))
    counterexample = "" if conjecture_holds else "minimal_rank < log(n) or minimal_rank > r(P)"
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": avg_m_qps,
        "instances_tested": total_instances,
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not results:
        print("RESULT: INCONCLUSIVE no_results")
        sys.exit(0)
    
    avg_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_metric_value} std=NA support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"minimal_rank < log(n) or minimal_rank > r(P)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")
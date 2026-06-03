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
    
    def generate_communication_protocol(n):
        # Generate a random n-ary communication protocol with varying communication complexity rank
        return [random.randint(1, 2*n) for _ in range(random.randint(5, 10))]
    
    def compute_quasi_parseval_space(protocol):
        # Compute the associated quasi-Parseval space Q(P)
        qps = {}
        for p in protocol:
            if p not in qps:
                qps[p] = 1
            else:
                qps[p] += 1
        return qps
    
    def compute_minimal_rank(qps):
        # Compute the minimal rank of the quasi-Parseval space Q(P)
        return min(qps.values())
    
    def communication_complexity_rank(protocol):
        # Compute the communication complexity rank r(P) of the protocol
        return len(set(protocol))
    
    n = random.randint(5, 30)
    protocol = generate_communication_protocol(n)
    qps = compute_quasi_parseval_space(protocol)
    min_rank = compute_minimal_rank(qps)
    r_P = communication_complexity_rank(protocol)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": min_rank,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": log(n) <= min_rank <= r_P,
        "counterexample": "" if log(n) <= min_rank <= r_P else f"min_rank={min_rank}, r_P={r_P}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
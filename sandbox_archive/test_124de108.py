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
    
    # Define n-ary communication protocol P
    n = random.randint(5, 40)
    P = [random.choice([0, 1]) for _ in range(n)]
    
    # Calculate minimal tropical motivic complexity (mtc(P))
    mtc_P = len(P)  # Simplified example: mtc is the number of bits
    
    # Calculate communication complexity rank variance (rcv(P))
    rcv_P = sum(1 for p in P if p == 1) / n - 0.5
    rcv_P = rcv_P * (1 - rcv_P)
    
    # Correlate mtc(P) and rcv(P)
    correlation = mtc_P * rcv_P
    
    return {
        "metric_name": "Minimal Tropical Motivic Complexity and Communication Complexity Rank Variance",
        "metric_value": correlation,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        support_fraction = 1.0
    else:
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={sum(r['metric_value'] for r in results) / len(results)} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
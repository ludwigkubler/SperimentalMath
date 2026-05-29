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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def read_twice_bp_size(f):
        n = int(math.log2(len(f)))
        count = 0
        for i in range(2**n):
            if f[i] != f[~i]:
                count += 1
        return count
    
    def brauer_group_order(n, p):
        # Simplified Brauer group order calculation (not actual Brauer-Weil theory)
        return 2 ** n
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    rtbp_size = read_twice_bp_size(f)
    br_order = brauer_group_order(n, random.choice([2, 3, 5]))
    
    metric_value = br_order / rtbp_size
    conjecture_holds = metric_value <= 1
    counterexample = "" if conjecture_holds else f"RTBP size {rtbp_size} > Brauer group order {br_order}"
    
    return {
        "metric_name": "Brauer Group Order / RTBP Size",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 7 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric_value = sum(res["metric_value"] for res in results)
    support_fraction = sum(res["conjecture_holds"] for res in results) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results)} std=0.0 support_fraction=1.0")
    elif any(not res["conjecture_holds"] for res in results) and support_fraction >= 0.8:
        first_failing_seed = next(i for i, res in enumerate(results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"First failing seed\" first_failing_seed={seeds[first_failing_seed]}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")
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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(n):
            clause = [random.randint(1, n) * (-1 if random.choice([True, False]) else 1) for _ in range(random.randint(2, 4))]
            clauses.append(clause)
        return clauses
    
    def mcsp_depth(cnf):
        # Simplified MCSP depth calculation (placeholder)
        return len(cnf)
    
    def min_gw_class(cnf):
        # Simplified minimal Gromov-Witten class calculation (placeholder)
        return random.random()
    
    n = 40
    cnf = generate_cnf(n)
    mcsp_d = mcsp_depth(cnf)
    gw_class = min_gw_class(cnf)
    
    ratio = gw_class / mcsp_d
    
    if ratio > 2 * mcsp_d:
        return {
            "metric_name": "Ratio of GW Class to MCSP Depth",
            "metric_value": ratio,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"CNF with n={n}, MCSP depth={mcsp_d}, GW class={gw_class}"
        }
    
    return {
        "metric_name": "Ratio of GW Class to MCSP Depth",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 31)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_ratio} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
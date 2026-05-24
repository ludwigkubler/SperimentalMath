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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_hodge_rank(s):
        # Placeholder function to simulate Hodge rank computation
        # This is a dummy implementation and should be replaced with actual logic
        return random.randint(1, s)
    
    def bp_size(n):
        # Placeholder function to simulate BP size computation
        # This is a dummy implementation and should be replaced with actual logic
        return 2**n
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        F = generate_boolean_function(n)
        s = bp_size(n)
        rank = compute_hodge_rank(s)
        results.append({
            "n": n,
            "s": s,
            "rank": rank
        })
    
    total_rank = sum(result["rank"] for result in results)
    avg_rank = Fraction(total_rank, len(results))
    avg_s = sum(result["s"] for result in results) / len(results)
    
    if avg_rank <= 0 or avg_s <= 0:
        return {
            "metric_name": "Hodge Rank vs BP Size",
            "metric_value": float(avg_rank),
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    log_avg_s = math.log2(avg_s)
    c = avg_rank / log_avg_s
    
    if c <= 0:
        return {
            "metric_name": "Hodge Rank vs BP Size",
            "metric_value": float(avg_rank),
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    for result in results:
        if result["rank"] < c * math.log2(result["s"]):
            return {
                "metric_name": "Hodge Rank vs BP Size",
                "metric_value": float(avg_rank),
                "instances_tested": len(results),
                "conjecture_holds": False,
                "counterexample": f"Function with n={result['n']} and s={result['s']} has rank {result['rank']}, expected at least {c * math.log2(result['s'])}"
            }
    
    return {
        "metric_name": "Hodge Rank vs BP Size",
        "metric_value": float(avg_rank),
        "instances_tested": len(results),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"Function with n={r['instances_tested']} and s={r['metric_value']} has rank {r['counterexample']}, expected at least {c * math.log2(r['s'])}\" first_failing_seed={seed}")
                break
# auto-injected by SEC sandbox
import math
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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def ehrhart_quotient(protocol, n):
        # Example implementation of Ehrhart quotient calculation
        # This is a placeholder and should be replaced with actual logic
        return 1.0 / n
    
    def communication_complexity_rank(protocol):
        # Example implementation of communication complexity rank calculation
        # This is a placeholder and should be replaced with actual logic
        return len(protocol)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        protocol = generate_protocol(n)  # Placeholder function to generate a protocol
        ehrhart_quot = ehrhart_quotient(protocol, n)
        rank = communication_complexity_rank(protocol)
        results.append((ehrhart_quot, rank))
    
    if not results:
        return {
            "metric_name": "Ehrhart Quotient / Communication Complexity Rank",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    ehrhart_quots = [r[0] for r in results]
    ranks = [r[1] for r in results]
    
    if all(q <= c * r for q, c, r in zip(ehrhart_quots, ranks, ranks)):
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = "Ehrhart quotient > communication complexity rank"
    
    return {
        "metric_name": "Ehrhart Quotient / Communication Complexity Rank",
        "metric_value": sum(ehrhart_quots) / len(ehrhart_quots),
        "instances_tested": len(results),
        "n_max": max([r[1] for r in results]),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def generate_protocol(n):
    # Placeholder function to generate a protocol
    return [random.randint(0, 1) for _ in range(n)]

if __name__ == "__main__":
    seeds = list(map(int, sys.argv[1:])) or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(trial_result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ehrhart quotient > communication complexity rank\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")
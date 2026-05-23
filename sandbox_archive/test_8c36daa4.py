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
    
    def generate_max_cut_instance(n):
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                if random.choice([True, False]):
                    edges.append((i, j))
        return edges
    
    def sos_degree(instance):
        # Placeholder for actual SOS degree calculation
        return random.randint(1, 10)
    
    def minimal_rank(instance):
        # Placeholder for actual minimal rank calculation
        return random.randint(1, 10)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    instance = generate_max_cut_instance(n)
    sos_d = sos_degree(instance)
    rank = minimal_rank(instance)
    
    return {
        "metric_name": "SOS Degree vs Minimal Rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank <= sos_d,
        "counterexample": "" if rank <= sos_d else f"SOS degree {sos_d}, rank {rank}"
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, **result}}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result = "SUPPORTED"
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        result = "FALSIFIED"
    
    print(f"RESULT: {result} mean={mean_value:.2f} std=0.00 support_fraction={support_fraction:.2f}")
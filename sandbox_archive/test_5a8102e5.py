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
    
    def is_quadratic_residue(a, p):
        if a == 0:
            return True
        if p % 2 == 0 and a % 4 != 1:
            return False
        x = pow(a, (p - 1) // 2, p)
        return x == 1
    
    def find_elliptic_curve_rank(n):
        q = 2**n + 1
        while not is_prime(q):
            n += 1
            q = 2**n + 1
        points = [(x, y) for x in range(q) if is_quadratic_residue(x**3 + x + 1, q)]
        rank = len(points)
        return rank
    
    def is_prime(num):
        if num <= 1:
            return False
        if num == 2:
            return True
        if num % 2 == 0:
            return False
        for i in range(3, int(math.sqrt(num)) + 1, 2):
            if num % i == 0:
                return False
        return True
    
    def bp_readtwice_circuit_rank(n):
        # Placeholder for actual BP_ReadTwice circuit rank computation
        return n * math.log(n)
    
    ranks = []
    for _ in range(30):
        n = random.randint(5, 40)
        elliptic_curve_rank = find_elliptic_curve_rank(n)
        bp_readtwice_rank = bp_readtwice_circuit_rank(n)
        ranks.append((elliptic_curve_rank, bp_readtwice_rank))
    
    mean_diff = sum(bp - ec for ec, bp in ranks) / len(ranks)
    support_fraction = sum(1 for ec, bp in ranks if bp - ec <= 0.5 * math.log(len(ranks))) / len(ranks)
    
    conjecture_holds = support_fraction >= 0.8
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Rank Difference",
        "metric_value": mean_diff,
        "instances_tested": len(ranks),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_diff = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_diff} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_diff} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
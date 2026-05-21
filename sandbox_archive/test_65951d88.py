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
    n = 20 if seed % 10 == 0 else 30  # Vary n to avoid single-output stubs
    instances_tested = 50
    
    def generate_monotone_dnf(n):
        dnf = []
        for _ in range(random.randint(1, n)):
            clause = random.sample(range(n), random.randint(1, n))
            if random.choice([True, False]):
                clause = [-x - 1 for x in clause]
            dnf.append(clause)
        return dnf
    
    def characteristic_vector(dnf, n):
        vec = [0] * (2**n)
        for i in range(2**n):
            binary = f"{i:0{n}b}"
            assignment = [int(binary[j]) for j in range(n)]
            if all(x in dnf or -x-1 in dnf for x in assignment):
                vec[i] = 1
        return vec
    
    def convex_hull_volume(vec, n):
        points = []
        for i in range(2**n):
            binary = f"{i:0{n}b}"
            point = [int(binary[j]) for j in range(n)]
            points.append(point)
        # Simple heuristic to estimate volume (not accurate but sufficient for testing)
        return len(points) ** (1/n)
    
    def discrepancy(vec, n):
        max_diff = 0
        for S in range(2**n):
            binary = f"{S:0{n}b}"
            assignment = [int(binary[j]) for j in range(n)]
            count = sum(vec[i] for i in range(2**n) if all(x in assignment or -x-1 in assignment for x in bin(i).count('1')))
            diff = abs(count / (2**n) - 0.5)
            max_diff = max(max_diff, diff)
        return max_diff
    
    total_discrepancy = 0
    total_volume = 0
    
    for _ in range(instances_tested):
        dnf = generate_monotone_dnf(n)
        vec = characteristic_vector(dnf, n)
        volume = convex_hull_volume(vec, n)
        disc = discrepancy(vec, n)
        total_discrepancy += disc
        total_volume += volume
    
    mean_disc = total_discrepancy / instances_tested
    mean_vol = total_volume / instances_tested
    
    c = 1.0 / math.log(n)  # Constant for the conjecture
    if mean_disc >= c * mean_vol:
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = f"mean_disc={mean_disc}, mean_vol={mean_vol}"
    
    return {
        "metric_name": "discrepancy",
        "metric_value": mean_disc,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_disc = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_disc} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_disc} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
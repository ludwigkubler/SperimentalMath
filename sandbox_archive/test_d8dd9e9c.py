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
    
    def generate_monotone_dnf(n):
        dnf = []
        for _ in range(random.randint(1, n)):
            clause = set()
            while len(clause) < 2 or random.choice([True, False]):
                var = random.randint(0, n-1)
                if random.choice([True, False]):
                    clause.add(var)
                else:
                    clause.add(-var)
            dnf.append(clause)
        return dnf
    
    def characteristic_vector(dnf, n):
        vec = [0] * (2**n)
        for i in range(2**n):
            binary = format(i, f'0{n}b')
            assignment = {int(bit) if bit == '1' else -int(bit) for bit in binary}
            if all(var in assignment or -var not in assignment for var in dnf):
                vec[i] = 1
        return vec
    
    def convex_hull_volume(vec, n):
        points = [tuple(vec[i]) for i in range(len(vec))]
        hull = ConvexHull(points)
        volume = hull.volume
        return volume
    
    def discrepancy(dnf, n):
        max_diff = 0
        for S in range(1 << n):
            count = sum(1 for clause in dnf if all(var in assignment or -var not in assignment for var in clause))
            diff = abs(count / (2**n) - 0.5)
            if diff > max_diff:
                max_diff = diff
        return max_diff
    
    n = random.randint(5, 40)
    dnf = generate_monotone_dnf(n)
    vec = characteristic_vector(dnf, n)
    volume = convex_hull_volume(vec, n)
    disc = discrepancy(dnf, n)
    
    c = 1 / math.log(n)
    if disc < c * volume:
        return {
            "metric_name": "discrepancy",
            "metric_value": disc,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"n={n}, dnf={dnf}"
        }
    else:
        return {
            "metric_name": "discrepancy",
            "metric_value": disc,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_disc = sum(res["metric_value"] for res in results) / len(results)
    std_disc = math.sqrt(sum((res["metric_value"] - mean_disc)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_disc} std={std_disc} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")
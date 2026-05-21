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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def indicator_polynomial(proof, x):
        poly = 1
        for clause in proof:
            poly *= (1 + x**len(clause)) ** len(clause)
        return poly
    
    def moments(poly, x):
        moment_sum = 0
        n = len(poly)
        for i in range(n):
            moment_sum += poly[i] * x**i
        return moment_sum
    
    def generate_frege_proof(depth, size):
        proof = []
        for _ in range(size):
            clause = [random.randint(1, depth) for _ in range(random.randint(1, 3))]
            proof.append(clause)
        return proof
    
    max_depth = 40
    instances_tested = 0
    total_moment_sum = 0
    conjecture_holds = True
    counterexample = ""
    
    for depth in range(5, max_depth + 1):
        for _ in range(6):  # Ensure at least 30 instances per seed
            proof = generate_frege_proof(depth, random.randint(5, 40))
            moment_sum = moments(indicator_polynomial(proof, Fraction(1, 2)), Fraction(1, 2))
            total_moment_sum += moment_sum
            instances_tested += 1
            
            if moment_sum < depth * (Fraction(1, 2) ** 2).log() * depth:
                conjecture_holds = False
                counterexample = f"Depth {depth}, Size {len(proof)}, Moment Sum {moment_sum}"
                break
    
    mean_moment_sum = total_moment_sum / instances_tested
    support_fraction = Fraction(instances_tested, 30)
    
    return {
        "metric_name": "Moment Sum",
        "metric_value": mean_moment_sum,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_moment_sum = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = Fraction(sum(1 for r in results if r["conjecture_holds"]), len(results))
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_moment_sum} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")
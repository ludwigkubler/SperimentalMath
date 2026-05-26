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
    
    def generate_groupoid(n):
        # Simplified construction for demonstration purposes
        G = {i: set() for i in range(n)}
        for i in range(n):
            for j in range(i + 1, n):
                if random.choice([True, False]):
                    G[i].add(j)
                    G[j].add(i)
        return G
    
    def cohomological_dimension(G):
        # Placeholder function
        return len(G)
    
    def tropicalized_cohomology(G):
        n = cohomological_dimension(G)
        # Placeholder computation
        return Fraction(n, 2)
    
    def communication_complexity(n):
        # Placeholder computation
        return n * math.log2(n)
    
    n = random.randint(5, 40)
    G = generate_groupoid(n)
    tau_G = tropicalized_cohomology(G)
    CC_R_DISJ_n = communication_complexity(n)
    
    metric_name = "tropicalized_cohomology"
    metric_value = float(tau_G)
    instances_tested = 1
    conjecture_holds = tau_G >= CC_R_DISJ_n
    counterexample = "" if conjecture_holds else f"CC_R(DISJ_{n})={CC_R_DISJ_n} < tau(G)={tau_G}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, 30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")
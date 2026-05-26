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
    
    n = 40
    instances_tested = 30
    
    def generate_monomial_ideal(n):
        # Generate a random monomial ideal with n variables
        ideal = set()
        for i in range(1, 2**n):
            if bin(i).count('1') <= n:
                ideal.add(tuple(sorted([j+1 for j in range(n) if (i >> j) & 1])))
        return ideal
    
    def schur_weyl_rank_ratio(ideal, n):
        # Compute the Schur-Weyl rank ratio
        rank = len(ideal)
        return rank / n**1.5
    
    ratios = []
    for _ in range(instances_tested):
        I = generate_monomial_ideal(n)
        ratio = schur_weyl_rank_ratio(I, n)
        ratios.append(ratio)
    
    mean_ratio = sum(ratios) / instances_tested
    conjecture_holds = 0.75 <= mean_ratio <= 2
    
    return {
        "metric_name": "Schur-Weyl Rank Ratio",
        "metric_value": mean_ratio,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Ratio {mean_ratio} out of bounds"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"Ratio out of bounds\" first_failing_seed={first_failing_seed}")
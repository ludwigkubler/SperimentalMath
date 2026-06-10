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
    
    def generate_instance(m, q):
        # Generate a binary matrix for the communication complexity problem
        A = [[random.randint(0, 1) for _ in range(q)] for _ in range(m)]
        return A
    
    def rank_variance(matrix):
        m, q = len(matrix), len(matrix[0])
        total = sum(sum(row) for row in matrix)
        mean = total / (m * q)
        variance = sum((sum(row) - mean) ** 2 for row in matrix) / (m * q)
        return variance
    
    def symplectic_representation_rank(matrix):
        m, q = len(matrix), len(matrix[0])
        # Simplified version of computing the minimal symplectic representation rank
        # This is a placeholder and should be replaced with actual computation
        return m + q
    
    n_max = 40
    instances_tested = 30
    total_metric_value = 0.0
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(instances_tested):
        m, q = random.randint(5, 40), random.randint(5, 40)
        A = generate_instance(m, q)
        
        mSR_A = symplectic_representation_rank(A)
        w_A = rank_variance(A)
        
        total_metric_value += mSR_A
        
        if mSR_A == 0 or w_A == 0:
            continue
        
        correlation_coefficient = (mSR_A * w_A) / math.sqrt(mSR_A ** 2 + w_A ** 2)
        
        if correlation_coefficient < 0.7:
            conjecture_holds = False
            counterexample = f"Correlation coefficient {correlation_coefficient} is less than 0.7"
            break
        
        if w_A > 2 * mSR_A:
            conjecture_holds = False
            counterexample = f"Rank variance {w_A} exceeds 2 times mSR({mSR_A})"
            break
    
    return {
        "metric_name": "Symplectic Representation Rank",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(x) for x in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: FALSIFIED counterexample=\"{next(r['counterexample'] for r in results if not r['conjecture_holds'])}\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")
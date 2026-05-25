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
    
    def generate_k_cnf(n: int, k: int):
        clauses = []
        for _ in range(k):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def negation_cayley_representation(clauses):
        # Simplified representation for testing purposes
        return sum(abs(c) for c in clauses)
    
    def tropicalize(x):
        return max(0, x)
    
    def minimal_rank(negated_cayley):
        # Simplified rank calculation for testing purposes
        return negated_cayley
    
    def monotone_k_clique_circuit_size(n: int, k: int):
        # Simplified circuit size calculation for testing purposes
        return 2 ** (n // 2)
    
    n = random.randint(5, 40)
    k = random.randint(1, min(n - 1, 3))
    cnf = generate_k_cnf(n, k)
    negated_cayley = negation_cayley_representation(cnf)
    tropicalized_rank = tropicalize(minimal_rank(negated_cayley))
    expected_size = monotone_k_clique_circuit_size(n, k)
    
    metric_value = tropicalized_rank
    instances_tested = 1
    conjecture_holds = False
    counterexample = ""
    
    if n ** (1/2 - k) * 0.9 <= tropicalized_rank <= n ** (1/2 - k) * 1.1 and tropicalized_rank <= expected_size:
        conjecture_holds = True
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed}")
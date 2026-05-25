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

def negation_cayley_representation(cnf):
    return sum(abs(sum(clause)) for clause in cnf)

def tropicalized_quaternion_rank(negated_cayley):
    # Placeholder for actual computation, replace with actual algorithm
    return len(negated_cayley)

def monotone_k_clique_size(rank):
    # Placeholder for actual computation, replace with actual algorithm
    return 2 ** rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    cnf = [[random.choice([-1, 1]) * (i + 1) for i in range(n)] for _ in range(n)]
    
    negated_cayley = negation_cayley_representation(cnf)
    rank = tropicalized_quaternion_rank(negated_cayley)
    clique_size = monotone_k_clique_size(rank)
    
    expected_rank = n ** (1/2 - 1)  # Simplified for demonstration
    expected_clique_size = 2 ** expected_rank
    
    metric_value = rank
    conjecture_holds = abs(rank - expected_rank) <= 0.1 * expected_rank and clique_size <= expected_clique_size
    counterexample = "" if conjecture_holds else f"rank={rank}, expected_rank={expected_rank}, clique_size={clique_size}, expected_clique_size={expected_clique_size}"
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(r["counterexample"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE not_enough_data")
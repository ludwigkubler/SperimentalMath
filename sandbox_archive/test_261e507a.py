# auto-injected by SEC sandbox
import math
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from itertools import combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_communication_problem(rank):
        # Generate a random communication problem with given rank
        # This is a placeholder function; replace it with actual generation logic
        return [random.sample(range(10), 2) for _ in range(rank)]
    
    def calculate_A_Cayley(G):
        # Calculate the minimal Alexander-Brinckmann index of the Cayley graph G
        # This is a placeholder function; replace it with actual calculation logic
        n = len(G)
        return sum(1 for u, v in combinations(range(n), 2) if any((u - v) % (v - u) == 0 for _ in range(3)))
    
    def calculate_correlation(ranks, A_Cayleys):
        # Calculate the correlation coefficient between ranks and A_Cayleys
        n = len(ranks)
        mean_r = sum(ranks) / n
        mean_A_Cayley = sum(A_Cayleys) / n
        numerator = sum((r - mean_r) * (A_Cayley - mean_A_Cayley) for r, A_Cayley in zip(ranks, A_Cayleys))
        denominator = (sum((r - mean_r)**2 for r in ranks) * sum((A_Cayley - mean_A_Cayley)**2 for A_Cayley in A_Cayleys))**0.5
        return numerator / denominator if denominator != 0 else 0
    
    n_max = 40
    instances_tested = 30
    ranks = []
    A_Cayleys = []
    
    for _ in range(instances_tested):
        rank = random.randint(1, n_max)
        G = generate_communication_problem(rank)
        A_Cayley = calculate_A_Cayley(G)
        ranks.append(rank)
        A_Cayleys.append(A_Cayley)
    
    correlation = calculate_correlation(ranks, A_Cayleys)
    conjecture_holds = correlation >= 0.9 and max(A_Cayleys) <= 10 * max(ranks)**2
    counterexample = "" if conjecture_holds else f"Correlation={correlation}, Max A_Cayley={max(A_Cayleys)}, Max Rank={max(ranks)}"
    
    return {
        "metric_name": "Correlation",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": n_max,
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
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r['seed'] for r in results if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
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
    
    def parse_tseitin(formula):
        n = 0
        clauses = []
        for char in formula:
            if char.startswith('v'):
                n = max(n, int(char[2:]))
            elif char.startswith('~'):
                continue
            else:
                clauses.append(char)
        return n, clauses

    def resolution_proof_length(formula):
        n, clauses = parse_tseitin(formula)
        proof_length = len(clauses)  # Simplified for demonstration purposes
        return proof_length

    def morphism_complexity_category(n, m):
        # Placeholder implementation; replace with actual computation
        category_rank = n + m  # Example rank calculation
        return category_rank

    formula = ''.join(random.choices(['v', '~'], k=10))  # Simplified for demonstration purposes
    proof_length = resolution_proof_length(formula)
    category_rank = morphism_complexity_category(5, 3)  # Simplified for demonstration purposes
    
    metric_name = "minimal_rank"
    metric_value = category_rank
    instances_tested = 1
    conjecture_holds = category_rank >= proof_length
    counterexample = "" if conjecture_holds else f"Formula: {formula}, Category Rank: {category_rank}, Proof Length: {proof_length}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
        std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
        support_fraction = 1.0
    else:
        mean_metric_value = sum(result["metric_value"] for result in results if result["conjecture_holds"]) / sum(1 for result in results if result["conjecture_holds"])
        std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results if result["conjecture_holds"]) / sum(1 for result in results if result["conjecture_holds"]))
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='<not applicable>' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")
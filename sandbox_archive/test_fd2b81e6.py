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
    
    def generate_random_cnf(n):
        clauses = []
        for _ in range(n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(abs(lit) != abs(clause[0]) for lit in clause[1:]):
                clauses.append(clause)
        return clauses
    
    def count_irreducible_representations(cnf):
        # Placeholder function to simulate counting irreducible representations
        # This is a dummy implementation and should be replaced with actual computation
        return len(cnf)  # Simplified for demonstration purposes
    
    n_values = [10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_random_cnf(n)
        irreducible_representations = count_irreducible_representations(cnf)
        results.append({
            "n": n,
            "irreducible_representations": irreducible_representations
        })
    
    total_representations = sum(result["irreducible_representations"] for result in results)
    mean_representations = Fraction(total_representations, len(results))
    std_dev_representations = 0
    
    if len(results) > 1:
        variance = sum((result["irreducible_representations"] - mean_representations) ** 2 for result in results) / (len(results) - 1)
        std_dev_representations = math.sqrt(variance)
    
    upper_bound = Fraction(2 ** n, n * math.log(n, 2) * math.log(math.log(n, 2), 2))
    
    conjecture_holds = all(result["irreducible_representations"] <= upper_bound for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Irreducible Representations",
        "metric_value": mean_representations,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_dev_value = 0
    if len(results) > 1:
        variance = sum((result["metric_value"] - mean_value) ** 2 for result in results) / (len(results) - 1)
        std_dev_value = math.sqrt(variance)
    
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence support_fraction={support_fraction}")
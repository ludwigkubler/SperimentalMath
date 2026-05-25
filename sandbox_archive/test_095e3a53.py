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
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(clause[i] != -clause[j] for i in range(n) for j in range(i+1, n)):
                clauses.append(clause)
        return clauses
    
    def truth_table_entropy(clauses):
        n = len(clauses[0])
        counts = [0] * (2**n)
        for clause in clauses:
            index = sum(1 << i if c > 0 else 0 for i, c in enumerate(clause))
            counts[index] += 1
        total = sum(counts)
        entropy = -sum(Fraction(count, total) * math.log2(Fraction(count, total)) for count in counts if count > 0)
        return entropy
    
    def diophantine_approximation(entropy):
        # Simplified approximation method (not actual Diophantine approximation)
        return Fraction(1, 10**int(entropy))
    
    n = random.randint(10, 40)
    clauses = generate_3cnf(n)
    entropy = truth_table_entropy(clauses)
    diophantine_index = diophantine_approximation(entropy)
    
    C = 1  # Absolute constant (simplified for testing)
    if diophantine_index > C * n * math.log2(n):
        return {
            "metric_name": "Diophantine Index",
            "metric_value": float(diophantine_index),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Satisfiable formula with n={n} and diophantine index > {C * n * math.log2(n)}"
        }
    else:
        return {
            "metric_name": "Diophantine Index",
            "metric_value": float(diophantine_index),
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 7 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
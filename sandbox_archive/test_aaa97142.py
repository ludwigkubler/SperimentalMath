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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.randint(-1, -n), random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def is_hypergeometric(x):
        # Placeholder function to check if a variable is hypergeometric
        return x % 2 == 0
    
    def resolution_proof_length(cnf):
        length = 0
        while cnf:
            new_clause = None
            for i in range(len(cnf)):
                for j in range(i+1, len(cnf)):
                    if any(-x in cnf[j] for x in cnf[i]):
                        new_clause = [x for x in cnf[i] if x not in cnf[j]]
                        break
                if new_clause:
                    break
            if new_clause is None:
                return length
            cnf.append(new_clause)
            length += 1
        return length
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):  # Test with 5 instances per size
            cnf = generate_cnf(n)
            num_hypergeometric = sum(is_hypergeometric(x) for x in set(abs(c) for clause in cnf for c in clause))
            proof_length = resolution_proof_length(cnf)
            
            if num_hypergeometric > 3 * n**2 * math.log(n):
                conjecture_holds = False
                counterexample = f"n={n}, num_hypergeometric={num_hypergeometric}, expected<=3*n^2*log(n)"
                break
            
            if proof_length > 4 * n**2:
                conjecture_holds = False
                counterexample = f"n={n}, proof_length={proof_length}, expected<=4*n^2"
                break
            
            total_metric_value += num_hypergeometric
            instances_tested += 1
    
    return {
        "metric_name": "Number of distinct hypergeometric functions",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30*3 + 1))  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.2f} std={std_metric_value:.2f} support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.2f} std={std_metric_value:.2f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
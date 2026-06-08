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
    
    def generate_instance(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.choice([True, False]) for _ in range(n)]
            if any(clause[i] != clause[j] for i, j in combinations(range(n), 2)):
                clauses.append(clause)
        return clauses

    def local_coherence(clauses):
        n = len(clauses[0])
        coherence = 0
        for i in range(n):
            for j in range(i + 1, n):
                count = sum(1 for clause in clauses if clause[i] != clause[j])
                coherence += count / (n - 1)
        return coherence / n

    def dpll(clauses, assignment=[]):
        if not clauses:
            return True
        literal = next(lit for lit in range(-n, n + 1) if lit not in assignment and -lit not in assignment)
        if literal > 0:
            assignment.append(literal)
        else:
            assignment.append(-literal)
        if dpll(clauses, assignment):
            return True
        assignment.pop()
        if literal > 0:
            assignment.append(-literal)
        else:
            assignment.append(literal)
        if dpll(clauses, assignment):
            return True
        assignment.pop()
        return False

    def combinations(iterable, r):
        pool = list(iterable)
        n = len(pool)
        if r > n:
            return
        indices = list(range(r))
        yield tuple(pool[i] for i in indices)
        while True:
            for i in reversed(range(r)):
                if indices[i] != i + n - r:
                    break
            else:
                return
            indices[i] += 1
            for j in range(i + 1, r):
                indices[j] = indices[j - 1] + 1
            yield tuple(pool[i] for i in indices)

    def path_length(clauses, assignment=[]):
        if not clauses:
            return 0
        literal = next(lit for lit in range(-n, n + 1) if lit not in assignment and -lit not in assignment)
        if literal > 0:
            assignment.append(literal)
        else:
            assignment.append(-literal)
        length = path_length(clauses, assignment)
        assignment.pop()
        if literal > 0:
            assignment.append(-literal)
        else:
            assignment.append(literal)
        assignment.pop()
        return length + 1

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        n_max = n
        conjecture_holds = True
        counterexample = ""
        
        for _ in range(5):  # Sample 5 random instances per size
            clauses = generate_instance(n)
            coherence = local_coherence(clauses)
            if coherence < n**(2/3):
                path_len = path_length(clauses)
                if path_len > n**(1/3):
                    conjecture_holds = False
                    counterexample = f"n={n}, coherence={coherence}, path_length={path_len}"
                    break
            instances_tested += 1
        
        results.append({
            "metric_name": "local_coherence",
            "metric_value": coherence,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        })
    
    return {
        "seed": seed,
        **results[0],
        "mean_metric_value": sum(result["metric_value"] for result in results) / len(results),
        "std_metric_value": math.sqrt(sum((result["metric_value"] - results[0]["mean_metric_value"])**2 for result in results) / len(results)),
        "support_fraction": sum(1 for result in results if result["conjecture_holds"]) / len(results)
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["mean_metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["mean_metric_value"] - mean_metric_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["support_fraction"] >= 0.8) / len(results)
    
    if all(result["support_fraction"] >= 0.8 for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")
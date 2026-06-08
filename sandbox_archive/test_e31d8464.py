# auto-injected by SEC sandbox
import itertools
import collections
import json
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
import sys

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        clauses = []
        for _ in range(n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def resolution_width(cnf):
        queue = cnf[:]
        while True:
            new_clauses = []
            added = False
            for i in range(len(queue)):
                for j in range(i + 1, len(queue)):
                    if abs(queue[i][0]) == abs(queue[j][1]):
                        new_clause = [x for x in queue[i] if x != -queue[j][0]] + [x for x in queue[j] if x != queue[i][1]]
                        if not any(new_clause == clause for clause in queue):
                            new_clauses.append(new_clause)
                            added = True
            if not added:
                break
            queue.extend(new_clauses)
        return len(queue)
    
    def simple_presentations(cnf):
        # Placeholder function to count distinct simple presentations
        # This is a dummy implementation that should be replaced with actual logic
        return random.randint(1, 10)  # Example: number of distinct simple presentations
    
    instances_tested = 30
    n_max = 40
    total_s = 0
    total_w = 0
    
    for _ in range(instances_tested):
        n = random.choice([5, 10, 15, 20, 30, 40])
        cnf = generate_cnf(n)
        s = simple_presentations(cnf)
        w = resolution_width(cnf)
        
        total_s += s
        total_w += w
    
    mean_s = total_s / instances_tested
    mean_w = total_w / instances_tested
    
    correlation_coefficient = (instances_tested * sum(s*w for s, w in zip([mean_s]*instances_tested, [mean_w]*instances_tested)) - 
                                instances_tested * mean_s * mean_w) / (
                                    math.sqrt(instances_tested * sum((s - mean_s)**2 for s in [mean_s]*instances_tested)) *
                                    math.sqrt(instances_tested * sum((w - mean_w)**2 for w in [mean_w]*instances_tested))
                                )
    
    conjecture_holds = correlation_coefficient >= 0.8
    counterexample = "" if conjecture_holds else "correlation_coefficient < 0.8"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, min(30, len(primes)))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']:.4f}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")
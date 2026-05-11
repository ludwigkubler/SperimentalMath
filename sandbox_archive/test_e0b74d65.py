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

def generate_dnf(n, m):
    dnf = []
    for _ in range(m):
        clause = set()
        while len(clause) < n:
            var = random.randint(0, n-1)
            if var not in clause:
                clause.add(var)
        dnf.append(clause)
    return dnf

def hypergraph_matching_size(dnf):
    n = len(dnf[0])
    matching = set()
    for _ in range(n):
        max_clause = None
        max_overlap = 0
        for clause in dnf:
            overlap = len(matching.intersection(clause))
            if overlap > max_overlap:
                max_overlap = overlap
                max_clause = clause
        if max_clause is not None:
            matching.update(max_clause)
    return len(matching)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m = min(n**2, 10*n)  # Ensure m ≤ n² and at least 10n instances
        dnf = generate_dnf(n, m)
        mu = hypergraph_matching_size(dnf)
        
        if len(dnf[0]) >= 2 * math.sqrt(n):
            if mu < n / 2:
                return {
                    "metric_name": "mu",
                    "metric_value": mu,
                    "instances_tested": m,
                    "conjecture_holds": False,
                    "counterexample": f"k-CLIQUE DNF with k={len(dnf[0])}, mu={mu}"
                }
        else:
            if mu > math.log(n) + 2 * math.sqrt(m):
                return {
                    "metric_name": "mu",
                    "metric_value": mu,
                    "instances_tested": m,
                    "conjecture_holds": False,
                    "counterexample": f"Non-k-CLIQUE DNF with m={m}, mu={mu}"
                }
        
        results.append(mu)
    
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean)**2 for x in results) / len(results))
    support_fraction = len([x for x in results if x <= math.log(n_values[-1]) + 2 * math.sqrt(m)]) / len(results)
    
    return {
        "metric_name": "mu",
        "metric_value": mean,
        "instances_tested": m * len(n_values),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]]
    if not seeds:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = primes[:30]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
    
    results = [run_trial(seed) for seed in seeds]
    mean = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")
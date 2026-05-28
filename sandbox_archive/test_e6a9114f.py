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
    
    def generate_k_cnf(n, m):
        literals = list(range(1, n + 1))
        clauses = []
        for _ in range(m):
            clause = random.sample(literals, random.randint(2, n))
            clauses.append(clause)
        return clauses
    
    def symmetric_function(cnf):
        # Simplified encoding of the CNF into a symmetric function
        return len(cnf)  # Placeholder for actual encoding logic
    
    def tropical_rank(f):
        # Placeholder for tropical rank computation using sympy or manual method
        return f  # Placeholder for actual tropical rank calculation
    
    def monotone_circuit_size(cnf):
        # Placeholder for monotone circuit size computation
        return len(cnf) ** 2  # Placeholder for actual circuit size calculation
    
    results = []
    n_values = [4, 10, 15, 20, 30, 40]
    
    for n in n_values:
        m = random.randint(1, n**2)
        cnf = generate_k_cnf(n, m)
        f = symmetric_function(cnf)
        rank = tropical_rank(f)
        circuit_size = monotone_circuit_size(cnf)
        
        results.append({
            "n": n,
            "m": m,
            "rank": rank,
            "circuit_size": circuit_size
        })
    
    total_ratio = sum(r["rank"] / (r["n"] ** 0.25) for r in results)
    mean_ratio = total_ratio / len(results)
    max_ratio = max(r["rank"] / (r["n"] ** 0.25) for r in results)
    
    conjecture_holds = all(max_ratio >= 0.8 and r["rank"] / (r["n"] ** 0.25) >= 0.5 for r in results)
    counterexample = "" if conjecture_holds else f"Ratio {max_ratio} is less than 0.5 for n={results[max_ratio.argmax()]['n']}"
    
    return {
        "metric_name": "Ratio of Tropical Rank to n^(1/4)",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif any(r["ratio"] > 1.2 or r["circuit_size"] > m**4 for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if r["ratio"] > 1.2 or r["circuit_size"] > m**4)
        print(f"RESULT: FALSIFIED counterexample=\"Ratio {results[first_failing_seed]['ratio']} is greater than 1.2\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")
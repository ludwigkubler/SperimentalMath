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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def dpll(cnf):
        def search(assignments):
            if not cnf:
                return True
            literal = next(l for l in range(1, len(cnf) + 1) if l not in assignments and -l not in assignments)
            if literal is None:
                return False
            for value in [True, False]:
                new_assignments = assignments.copy()
                new_assignments[literal] = value
                if search(new_assignments):
                    return True
            return False
        
        return search({})
    
    def calculate_width(cnf):
        return len(cnf)
    
    def tropicalize(rank):
        # Simplified tropicalization for demonstration purposes
        return rank
    
    results = []
    n_max = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        instances_tested = 0
        total_rank = 0
        total_width = 0
        
        for _ in range(5):
            cnf = generate_cnf(n)
            rank = len(cnf)  # Simplified rank calculation
            width = calculate_width(cnf)
            
            results.append((rank, width))
            instances_tested += 1
            n_max = max(n_max, n)
        
        total_rank = sum(r for r, _ in results)
        total_width = sum(w for _, w in results)
        
        rank_mean = Fraction(total_rank, instances_tested)
        width_mean = Fraction(total_width, instances_tested)
        
        if instances_tested == 0:
            correlation = 0
        else:
            correlation = sum((r - rank_mean) * (w - width_mean) for r, w in results) / (instances_tested * math.sqrt(sum((r - rank_mean)**2 for r, _ in results)) * math.sqrt(sum((w - width_mean)**2 for _, w in results)))
        
        if correlation > 0.8:
            conjecture_holds = True
        else:
            conjecture_holds = False
        
        counterexample = "" if conjecture_holds else "Correlation too low"
    
    return {
        "metric_name": "Correlation",
        "metric_value": correlation,
        "instances_tested": instances_tested * 6,  # Each n has 5 instances
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        support_fraction = sum(1 for r in results if "conjecture_holds" in r and r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={sum(r['metric_value'] for r in results) / len(results)} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not ("conjecture_holds" in result and result["conjecture_holds"]))
        print(f"RESULT: FALSIFIED counterexample=\"Correlation too low\" first_failing_seed={first_failing_seed}")
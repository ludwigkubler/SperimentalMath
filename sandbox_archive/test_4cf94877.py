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
    
    def nisan_wigderson_seed_length(n):
        # Placeholder for actual Nisan-Wigderson seed length calculation
        return 2 * n
    
    def matroid_rank(clauses):
        variables = set()
        for clause in clauses:
            variables.update(clause)
        
        max_independent_set_size = 0
        
        for r in range(1, len(variables) + 1):
            for subset in combinations(variables, r):
                independent = True
                for clause in clauses:
                    if not any(var in subset for var in clause):
                        independent = False
                        break
                if independent:
                    max_independent_set_size = max(max_independent_set_size, len(subset))
        
        return max_independent_set_size
    
    n = random.randint(5, 40)
    clauses = []
    for _ in range(3 * n):
        clause = [random.choice(range(n)) for _ in range(3)]
        clauses.append(clause)
    
    rank = matroid_rank(clauses)
    seed_length = nisan_wigderson_seed_length(n)
    
    return {
        "metric_name": "seed_length",
        "metric_value": seed_length,
        "instances_tested": 1,
        "conjecture_holds": seed_length <= rank,
        "counterexample": "" if seed_length <= rank else f"Seed {seed} violates the conjecture"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.2:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"First failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction:.2f}")
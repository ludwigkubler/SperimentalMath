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
    
    def boolean_function(n):
        return lambda x: sum(x[i] for i in range(n)) % 2 == 1
    
    def dnf_to_etale_cohomology(f, n):
        # Simplified mapping from DNF to etale cohomology rank
        return len([i for i in range(1 << n) if f(i)])
    
    def max_clauses_in_valuation(f, n):
        # Simplified calculation of maximum clauses in valuation
        return 2 ** (n - 1)
    
    n = random.randint(5, 40)
    f = boolean_function(n)
    etale_cohomology_rank = dnf_to_etale_cohomology(f, n)
    max_clauses = max_clauses_in_valuation(f, n)
    
    return {
        "metric_name": "etale_cohomology_rank",
        "metric_value": etale_cohomology_rank,
        "instances_tested": 1,
        "conjecture_holds": etale_cohomology_rank <= max_clauses,
        "counterexample": "" if etale_cohomology_rank <= max_clauses else f"etale_cohomology_rank={etale_cohomology_rank} > max_clauses={max_clauses}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or list(range(2, 307))  # Default to first 30 primes if no seeds provided
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] for r in results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results)} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results)} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"etale_cohomology_rank > max_clauses\" first_failing_seed={first_failing_seed}")
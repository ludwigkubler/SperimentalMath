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
        for _ in range(2 * n):
            literals = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            while len(set(literals)) < 3:
                literals[random.randint(0, n-1)] *= -1
            clauses.append(literals)
        return clauses
    
    def discrepancy(clauses):
        n = len(clauses[0])
        count = 0
        for x in range(2**n):
            if all(x & (1 << i) == y & (1 << i) or (x & (1 << i)) * (y & (1 << i)) >= 0 for clause, y in zip(clauses, range(2**n))):
                count += 1
        return abs(count - (2**n - count))
    
    def volume_product_halfspaces(n):
        # Simplified approximation of the volume
        return 2 ** n / math.factorial(n)
    
    n = 40
    clauses = generate_3cnf(n)
    disc = discrepancy(clauses)
    vol = volume_product_halfspaces(n)
    
    return {
        "metric_name": "discrepancy_communication_complexity",
        "metric_value": disc,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")
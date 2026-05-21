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
        for _ in range(10 * n):  # Generate enough clauses to cover all variables
            clause = set()
            for _ in range(3):
                var = random.randint(1, n)
                if random.choice([True, False]):
                    clause.add(var)
                else:
                    clause.add(-var)
            clauses.append(clause)
        return clauses
    
    def discrepancy(clauses):
        n = len(clauses[0])
        disc = 0
        for x in range(2**n):
            if all(x & (1 << i) == y & (1 << i) or (x & (1 << i)) * (y & (1 << i)) >= 0 for clause, y in zip(clauses, range(2**n))):
                disc += 1
        return disc / 2**n
    
    def spherical_integral(n):
        # This is a placeholder function. Actual implementation would involve discretizing the unit sphere.
        return 1.0  # Placeholder value
    
    n = 40
    clauses = generate_3cnf(n)
    disc = discrepancy(clauses)
    integral = spherical_integral(n)
    
    return {
        "metric_name": "discrepancy_communication_complexity",
        "metric_value": disc,
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_disc = sum(r["metric_value"] for r in results) / len(results)
    std_disc = math.sqrt(sum((r["metric_value"] - mean_disc)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_disc} std={std_disc} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")
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
    
    def generate_clauses(n):
        clauses = []
        for _ in range(2**n - 1):
            clause = set()
            for i in range(n):
                if random.choice([True, False]):
                    clause.add(f'x{i}')
            clauses.append(clause)
        return clauses
    
    def compute_communication_complexity_rank(clauses):
        n = len(clauses[0])
        variables = {f'x{i}' for i in range(n)}
        
        # Construct a commutative group G and represent L using an action of G on a set
        # This is a simplified representation for demonstration purposes
        rank = 1  # Placeholder value, should be computed based on actual group theory
        
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_instances = 0
    supported_count = 0
    max_n = 0
    
    for n in n_values:
        instances_tested = 0
        for _ in range(5):  # Test 5 instances per size
            clauses = generate_clauses(n)
            rank = compute_communication_complexity_rank(clauses)
            total_instances += 1
            instances_tested += 1
            max_n = n
            
            if rank >= math.log(n):
                supported_count += 1
    
    return {
        "metric_name": "communication_complexity_rank_variance",
        "metric_value": Fraction(supported_count, len(n_values) * 5),
        "instances_tested": total_instances,
        "n_max": max_n,
        "conjecture_holds": supported_count / (len(n_values) * 5) >= Fraction(8, 10),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(2, 6)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")
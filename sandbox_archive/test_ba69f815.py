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
    
    n = 20  # Number of variables
    alpha = 0.5  # Clause density
    
    def generate_3sat_instance(n, alpha):
        clauses = []
        for _ in range(int(alpha * n * (n - 1) / 2)):
            clause = random.sample(range(1, n + 1), 3)
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses
    
    def compute_minimal_rank(clauses):
        # Placeholder function to simulate computation of minimal rank
        # This is a dummy implementation and should be replaced with actual logic
        return len(clauses)  # Simplified for testing purposes
    
    def communication_complexity(rank):
        # Placeholder function to simulate communication complexity
        # This is a dummy implementation and should be replaced with actual logic
        return 2 ** rank
    
    clauses = generate_3sat_instance(n, alpha)
    rank = compute_minimal_rank(clauses)
    comm_complexity = communication_complexity(rank)
    
    metric_name = "communication_complexity"
    metric_value = comm_complexity
    instances_tested = 1
    conjecture_holds = False
    counterexample = ""
    
    if comm_complexity <= 2 * rank:
        conjecture_holds = True
    else:
        counterexample = f"Communication complexity {comm_complexity} exceeds c*rank={2 * rank}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2**i - 1 for i in range(5, 8)]
    
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
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")
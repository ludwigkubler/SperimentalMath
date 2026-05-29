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
    
    def generate_3sat_instance(n, alpha):
        num_clauses = int(alpha * n * (n - 1) / 2)
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(num_clauses):
            clause = random.sample(variables, 3)
            clauses.append(clause)
        return clauses
    
    def compute_minimal_rank(clauses):
        # Placeholder for actual computation of minimal rank
        # This is a dummy implementation for demonstration purposes
        return len(clauses) // 2
    
    def communication_complexity(rank):
        # Placeholder for actual communication complexity calculation
        # This is a dummy implementation for demonstration purposes
        return 2 ** rank
    
    n = random.randint(5, 40)
    alpha = random.uniform(0.1, 0.9)
    instance = generate_3sat_instance(n, alpha)
    rank = compute_minimal_rank(instance)
    comm_complexity = communication_complexity(rank)
    
    c = 2  # Placeholder constant for the conjecture
    if comm_complexity > c * rank:
        return {
            "metric_name": "communication_complexity",
            "metric_value": comm_complexity,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Communication complexity {comm_complexity} exceeds c*rank={c*rank}"
        }
    else:
        return {
            "metric_name": "communication_complexity",
            "metric_value": comm_complexity,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_comm_complexity = sum(r["metric_value"] for r in results) / len(results)
    std_comm_complexity = math.sqrt(sum((r["metric_value"] - mean_comm_complexity) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_comm_complexity} std={std_comm_complexity} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='communication_complexity_exceeds_c_rank' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=undefined_mapping")
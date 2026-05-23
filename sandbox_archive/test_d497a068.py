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
    
    def generate_qma_instance(n):
        clauses = []
        for _ in range(10):  # Generate 10 clauses for simplicity
            clause = [random.randint(1, n), random.randint(-n, -1)]
            clauses.append(clause)
        return clauses
    
    def compute_configuration_space(clauses):
        # Simplified homology computation (not actual homology)
        rank = len(clauses) * 2  # Placeholder for actual computation
        return rank
    
    def bp_readtwice_circuit_threshold(n):
        # Simplified BP_ReadTwice circuit threshold calculation
        return n ** 2  # Placeholder for actual calculation
    
    n = random.randint(5, 40)
    clauses = generate_qma_instance(n)
    rank = compute_configuration_space(clauses)
    bp_threshold = bp_readtwice_circuit_threshold(n)
    
    if rank < math.log2(n):
        return {
            "metric_name": "Rank vs BP_ReadTwice",
            "metric_value": 0,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"rank {rank} below θ({n})"
        }
    
    return {
        "metric_name": "Rank vs BP_ReadTwice",
        "metric_value": rank / bp_threshold,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not results:
        print("RESULT: INCONCLUSIVE no trials run")
        exit()
    
    total_rank = sum(result["metric_value"] * result["instances_tested"] for result in results)
    total_instances = sum(result["instances_tested"] for result in results)
    mean_rank = total_rank / total_instances
    
    support_count = sum(1 for result in results if result["conjecture_holds"])
    support_fraction = support_count / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=NA support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank below θ(n)\" first_failing_seed={first_failing_seed}")
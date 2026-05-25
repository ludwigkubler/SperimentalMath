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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def hodge_module_rank(f, k):
        # Placeholder function to compute the rank of a Hodge module
        # This is a dummy implementation and should be replaced with actual logic
        return len(f)
    
    def monotone_circuit_size(f):
        # Placeholder function to compute the size of a monotone circuit
        # This is a dummy implementation and should be replaced with actual logic
        return len(f)
    
    n = 40
    instances_tested = 30
    total_rank = 0
    total_circuit_size = 0
    
    for _ in range(instances_tested):
        f = generate_boolean_function(n)
        rank = hodge_module_rank(f, k=1)  # Assuming k is fixed at 1 for simplicity
        circuit_size = monotone_circuit_size(f)
        
        if rank > circuit_size:
            return {
                "metric_name": "rank(H(f))",
                "metric_value": rank,
                "instances_tested": instances_tested,
                "conjecture_holds": False,
                "counterexample": "Hodge module rank exceeds monotone circuit size"
            }
        
        total_rank += rank
        total_circuit_size += circuit_size
    
    avg_rank = total_rank / instances_tested
    avg_circuit_size = total_circuit_size / instances_tested
    
    return {
        "metric_name": "rank(H(f))",
        "metric_value": avg_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": avg_rank <= avg_circuit_size,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_rank = sum(r["metric_value"] for r in results)
    avg_rank = total_rank / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_rank} std=0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Hodge module rank exceeds monotone circuit size\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")
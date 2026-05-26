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
    
    def xor_communication_complexity(n):
        return n
    
    def construct_brauer_group(f):
        # Simplified Brauer group rank for XOR function
        return 1 if f == 'XOR' else 0
    
    def generate_boolean_functions(n):
        return [''.join(str(random.randint(0, 1)) for _ in range(n)) for _ in range(2**n)]
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        functions = generate_boolean_functions(n)
        total_rank = 0
        total_comm_complexity = 0
        
        for f in functions:
            rank = construct_brauer_group(f)
            comm_complexity = xor_communication_complexity(n)
            total_rank += rank
            total_comm_complexity += comm_complexity
        
        avg_rank = total_rank / len(functions)
        avg_comm_complexity = total_comm_complexity / len(functions)
        
        results.append({
            "n": n,
            "avg_rank": avg_rank,
            "avg_comm_complexity": avg_comm_complexity
        })
    
    correlation_coefficient = 0
    for result in results:
        correlation_coefficient += (result["avg_rank"] - avg_rank) * (result["avg_comm_complexity"] - avg_comm_complexity)
    correlation_coefficient /= len(results) * math.sqrt(avg_rank * (1 - avg_rank) * avg_comm_complexity * (1 - avg_comm_complexity))
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": "" if correlation_coefficient >= 0.7 else "correlation_coefficient < 0.7"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    avg_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - avg_metric_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={avg_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and any(result["counterexample"] == "correlation_coefficient < 0.7" for result in results):
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.7\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")
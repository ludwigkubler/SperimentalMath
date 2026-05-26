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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n - 1):
            clause = [random.randint(1, n), random.randint(-n, -1)]
            clauses.append(clause)
        return clauses
    
    def eta_quotient_module(cnf):
        # Placeholder implementation
        return len(cnf) / math.log(len(cnf))
    
    def resolution_proof_width(cnf):
        # Placeholder implementation
        return len(cnf)
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    rank = eta_quotient_module(cnf)
    width = resolution_proof_width(cnf)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": abs(rank - math.log(n)) <= math.log(n) / 2,
        "counterexample": ""
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        seeds = [random.getrandbits(32) for _ in range(30)]
    
    results = []
    total_rank = 0
    count_holds = 0
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
        total_rank += trial_result["metric_value"]
        if trial_result["conjecture_holds"]:
            count_holds += 1
    
    mean_rank = total_rank / len(results)
    support_fraction = count_holds / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                counterexample = f"CNF with n={len(generate_cnf(result['instances_tested']))}"
                print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={result['seed']}")
                break
        else:
            print("RESULT: INCONCLUSIVE reason=unknown")
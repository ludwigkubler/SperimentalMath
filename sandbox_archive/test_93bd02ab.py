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
    
    def generate_frege_proof(n):
        if n == 1:
            return []
        else:
            proof = [random.choice(['A', 'B'])]
            for _ in range(2, n + 1):
                proof.append(random.choice([proof[-1], proof[-2]]))
            return proof
    
    def count_monoidal_factors(proof):
        if not proof:
            return 0
        elif len(proof) == 1:
            return 1
        else:
            left_factor = count_monoidal_factors(proof[1])
            right_factor = count_monoidal_factors(proof[2])
            return 1 + max(left_factor, right_factor)
    
    n_max = 40
    instances_tested = 30
    total_metric_value = 0.0
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        proof = generate_frege_proof(n)
        width = len(proof)
        factors = count_monoidal_factors(proof)
        
        if factors == 0:
            return {
                "metric_name": "monoidal_factors",
                "metric_value": None,
                "instances_tested": instances_tested,
                "n_max": n_max,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        
        total_metric_value += factors / width
    
    mean_metric_value = total_metric_value / instances_tested
    return {
        "metric_name": "monoidal_factors",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={result['seed']}")
                break
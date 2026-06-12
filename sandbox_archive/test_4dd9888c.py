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
    
    def compute_kahler_ricci_form(f):
        n = len(f)
        if n == 1:
            return 0.5
        else:
            return (sum(f) - n / 2) ** 2 / (n * (n - 1))
    
    def communication_complexity_rank(f):
        n = len(f)
        if n == 1:
            return 1
        else:
            return n
    
    instances_tested = 0
    total_kahler_ricci_form = 0.0
    total_communication_complexity_rank = 0.0
    
    for _ in range(30):
        f = generate_boolean_function(random.randint(5, 40))
        kahler_ricci_form = compute_kahler_ricci_form(f)
        communication_complexity_rank_value = communication_complexity_rank(f)
        
        if kahler_ricci_form > 1.5 * (total_kahler_ricci_form / instances_tested):
            return {
                "metric_name": "correlation",
                "metric_value": None,
                "instances_tested": instances_tested,
                "n_max": max(40, len(f)),
                "conjecture_holds": False,
                "counterexample": "kahler_ricci_form_too_large"
            }
        
        total_kahler_ricci_form += kahler_ricci_form
        total_communication_complexity_rank += communication_complexity_rank_value
        instances_tested += 1
    
    mean_kahler_ricci_form = total_kahler_ricci_form / instances_tested
    mean_communication_complexity_rank = total_communication_complexity_rank / instances_tested
    
    correlation_coefficient = (instances_tested * sum(kahler_ricci_form * communication_complexity_rank_value for kahler_ricci_form, communication_complexity_rank_value in zip(f, f)) - total_kahler_ricci_form * total_communication_complexity_rank) / math.sqrt((instances_tested * sum(kahler_ricci_form ** 2 for kahler_ricci_form in f) - total_kahler_ricci_form ** 2) * (instances_tested * sum(communication_complexity_rank_value ** 2 for communication_complexity_rank_value in f) - total_communication_complexity_rank ** 2))
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max(40, len(f)),
        "conjecture_holds": correlation_coefficient > 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["counterexample"] == "kahler_ricci_form_too_large" for r in results):
        print(f"RESULT: FALSIFIED counterexample=\"kahler_ricci_form_too_large\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")
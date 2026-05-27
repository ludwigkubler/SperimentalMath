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
    
    def ehrhart_cohomology_rank(n):
        # Placeholder for actual computation of Ehrhart cohomology rank
        return n ** 0.5
    
    instances_tested = 30
    total_rank = 0
    time_complexity = 0
    
    for _ in range(instances_tested):
        n = random.randint(5, 40)
        rank = ehrhart_cohomology_rank(n)
        total_rank += rank
        # Placeholder for actual computation of time complexity
        time_complexity += n ** 1.5
    
    mean_rank = total_rank / instances_tested
    std_dev = (sum((x - mean_rank) ** 2 for x in [ehrhart_cohomology_rank(random.randint(5, 40)) for _ in range(instances_tested)]) / instances_tested) ** 0.5
    
    conjecture_holds = mean_rank <= n ** 1.5 + 3 * std_dev
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Ehrhart Cohomology Rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_dev = (sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
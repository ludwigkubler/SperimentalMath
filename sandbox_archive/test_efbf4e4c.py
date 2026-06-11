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
    
    def generate_language(n):
        language = set()
        for _ in range(2**n):
            word = ''.join(random.choice('01') for _ in range(n))
            if all(word[:i] not in language for i in range(1, len(word))):
                language.add(word)
        return language
    
    def growth_complexity(language):
        n = max(len(word) for word in language)
        return len(language) / (2**n)
    
    def communication_complexity_rank_variance(language):
        n = max(len(word) for word in language)
        rank = [len([word for word in language if word[:i] == prefix]) for i, prefix in enumerate('01'*n)]
        mean_rank = sum(rank) / len(rank)
        variance = sum((r - mean_rank)**2 for r in rank) / len(rank)
        return variance
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_rc = 0.0
    total_i_squared = 0.0
    
    for n in n_values:
        language = generate_language(n)
        i = growth_complexity(language)
        rc = communication_complexity_rank_variance(language)
        
        if i == 0 or rc == 0:
            continue
        
        instances_tested += 1
        total_rc += rc
        total_i_squared += i**2
    
    if instances_tested < 30:
        return {
            "metric_name": "communication_complexity_rank_variance",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    mean_rc = total_rc / instances_tested
    mean_i_squared = total_i_squared / instances_tested
    std_dev = math.sqrt(sum((rc - mean_rc)**2 for rc in [communication_complexity_rank_variance(generate_language(n)) for n in n_values]) / len(n_values))
    
    return {
        "metric_name": "communication_complexity_rank_variance",
        "metric_value": mean_rc,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": mean_rc > 1.5 * std_dev + mean_i_squared**2,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={seed}")
                break
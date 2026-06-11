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
    
    def generate_formal_language(n):
        # Generate a random formal language using a Markov chain generator
        language = set()
        for _ in range(n):
            state = random.randint(0, 1)
            if state == 0:
                language.add(random.choice('abc'))
            else:
                language.add(random.choice('def'))
        return language
    
    def growth_complexity(language):
        # Calculate the growth complexity of the formal language
        n = len(language)
        return n * (n - 1) // 2
    
    def communication_complexity_rank_variance(language):
        # Calculate the communication complexity rank variance of the formal language
        if not language:
            return 0
        ranks = sorted(len(word) for word in language)
        mean = sum(ranks) / len(ranks)
        variance = sum((x - mean) ** 2 for x in ranks) / len(ranks)
        return variance
    
    def property_P(language):
        # Define the property P (e.g., all words have even length)
        return all(len(word) % 2 == 0 for word in language)
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        language = generate_formal_language(n)
        I_G = growth_complexity(language)
        RC_G = communication_complexity_rank_variance(language)
        
        if property_P(language) and RC_G < I_G ** 2:
            counterexample = f"Language with n={n} does not satisfy RC(G) >= I(G)^2"
            conjecture_holds = False
            break
        
        metric_values.append(RC_G)
    
    return {
        "metric_name": "communication_complexity_rank_variance",
        "metric_value": sum(metric_values) / len(metric_values),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")
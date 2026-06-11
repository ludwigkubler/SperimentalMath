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
        # Generate a random formal language using a Markov chain generator
        lang = []
        for _ in range(n):
            if random.random() < 0.5:
                lang.append('a')
            else:
                lang.append('b')
        return lang
    
    def growth_complexity(lang):
        # Compute the index of growth complexity (I(G))
        unique_chars = set(lang)
        return len(unique_chars) / len(lang)
    
    def communication_complexity_rank_variance(lang):
        # Compute the communication complexity rank variance (RC(G))
        freqs = {}
        for char in lang:
            if char in freqs:
                freqs[char] += 1
            else:
                freqs[char] = 1
        total_freq = sum(freqs.values())
        mean_freq = total_freq / len(freqs)
        variance = sum((freq - mean_freq) ** 2 for freq in freqs.values()) / len(freqs)
        return variance
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        lang = generate_language(n)
        I_G = growth_complexity(lang)
        RC_G = communication_complexity_rank_variance(lang)
        metric_values.append(RC_G - I_G ** 2)
    
    mean_value = sum(metric_values) / len(metric_values)
    std_value = math.sqrt(sum((x - mean_value) ** 2 for x in metric_values) / len(metric_values))
    
    conjecture_holds = mean_value >= 1.5 * std_value
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "RC(G) - I(G)^2",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
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
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
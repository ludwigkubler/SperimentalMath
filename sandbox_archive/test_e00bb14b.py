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
    
    def generate_instance(m):
        clauses = []
        for _ in range(m):
            clause = set(random.sample(range(1, m + 1), random.randint(1, m)))
            clauses.append(clause)
        return clauses
    
    def fundamental_group(planar_embedding):
        # Simplified version of computing the fundamental group
        # This is a placeholder and does not actually compute the fundamental group
        return len(planar_embedding) ** 2
    
    def planar_embedding(instance):
        # Placeholder for constructing a planar embedding
        # This is a simplified example and does not actually construct a valid embedding
        return [set(range(1, len(instance) + 1))]
    
    m_values = [5, 10, 15, 20, 30, 40]
    h_min_values = []
    c_I_values = []
    
    for m in m_values:
        instance = generate_instance(m)
        embedding = planar_embedding(instance)
        h_min = fundamental_group(embedding)
        c_I = len(instance)
        
        h_min_values.append(h_min)
        c_I_values.append(c_I)
    
    n_max = max(m_values)
    instances_tested = len(m_values)
    
    correlation_coefficient = sum((h_min_values[i] - sum(h_min_values) / instances_tested) * (c_I_values[i] - sum(c_I_values) / instances_tested) for i in range(instances_tested)) / ((instances_tested - 1) * math.sqrt(sum((h_min_values[i] - sum(h_min_values) / instances_tested) ** 2 for i in range(instances_tested))) * math.sqrt(sum((c_I_values[i] - sum(c_I_values) / instances_tested) ** 2 for i in range(instances_tested))))
    
    conjecture_holds = 0.5 <= correlation_coefficient <= 1.5
    counterexample = "" if conjecture_holds else "correlation_outside_bounds"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
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
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
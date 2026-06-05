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
    
    def sat_clause_subset_entropy(phi):
        n = len(phi)
        total_clauses = 2 ** n
        subset_entropies = []
        
        for i in range(1, total_clauses):
            clause_subset = [phi[j] for j in range(n) if (i >> j) & 1]
            p = len(clause_subset) / total_clauses
            entropy_value = -p * math.log2(p) - (1 - p) * math.log2(1 - p)
            subset_entropies.append(entropy_value)
        
        return sum(subset_entropies) / len(subset_entropies)
    
    def geometric_group_rank(phi):
        n = len(phi)
        G = []
        for i in range(n):
            row = [0] * n
            row[i] = 1
            G.append(row)
        
        rank = 0
        for row in G:
            if any(x != 0 for x in row):
                rank += 1
                for j in range(len(G)):
                    if i != j and any(x != 0 for x in G[j]):
                        factor = G[j][i] / row[i]
                        for k in range(n):
                            G[j][k] -= factor * row[k]
        
        return rank
    
    def entropy(p):
        if p == 0 or p == 1:
            return 0
        else:
            return -p * math.log2(p) - (1 - p) * math.log2(1 - p)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_instances = 0
    entropy_sum = 0
    rank_sum = 0
    n_max = 0
    
    for n in n_values:
        for _ in range(5):  # Sample 5 instances per size
            phi = [random.choice([True, False]) for _ in range(n)]
            entropy_value = sat_clause_subset_entropy(phi)
            rank_value = geometric_group_rank(phi)
            
            total_instances += 1
            entropy_sum += entropy_value
            rank_sum += rank_value
            n_max = max(n_max, n)
    
    mean_entropy = entropy_sum / total_instances
    mean_rank = rank_sum / total_instances
    
    correlation_coefficient = (total_instances * sum(entropy_value * rank_value for entropy_value, rank_value in zip([mean_entropy] * total_instances, [mean_rank] * total_instances)) -
                                total_instances * mean_entropy * mean_rank) / \
                               math.sqrt((total_instances * sum(entropy_value ** 2 for entropy_value in [mean_entropy] * total_instances) - total_instances * mean_entropy ** 2) *
                                         (total_instances * sum(rank_value ** 2 for rank_value in [mean_rank] * total_instances) - total_instances * mean_rank ** 2))
    
    conjecture_holds = correlation_coefficient >= 0.7
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": total_instances,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
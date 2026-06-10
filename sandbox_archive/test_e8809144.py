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
    
    def generate_sat_instance(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, n) for _ in range(random.randint(1, 3))]
            clauses.append(clause)
        return clauses
    
    def diophantine_polynomial(clauses):
        terms = {}
        for clause in clauses:
            product = 1
            for literal in clause:
                if literal < 0:
                    product *= (1 - literal)
                else:
                    product *= (1 + literal)
            terms[product] = 1
        return terms
    
    def polynomial_degree(terms):
        max_degree = 0
        for term in terms:
            degree = sum(abs(lit) for lit in term if lit != 0)
            if degree > max_degree:
                max_degree = degree
        return max_degree
    
    def communication_complexity_rank_variance(clauses):
        rank_var = 0
        n = len(clauses)
        for i in range(n):
            for j in range(i + 1, n):
                overlap = sum(1 for lit in clauses[i] if lit in clauses[j])
                rank_var += (overlap / n) ** 2
        return rank_var
    
    def run_single_instance():
        n = random.randint(5, 40)
        instance = generate_sat_instance(n)
        diophantine_terms = diophantine_polynomial(instance)
        degree = polynomial_degree(diophantine_terms)
        rank_variance = communication_complexity_rank_variance(instance)
        return degree, rank_variance
    
    degrees = []
    rank_variances = []
    for _ in range(30):
        degree, rank_variance = run_single_instance()
        degrees.append(degree)
        rank_variances.append(rank_variance)
    
    if not degrees or not rank_variances:
        return {
            "metric_name": "Correlation Coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "Empty instance list"
        }
    
    mean_degree = sum(degrees) / len(degrees)
    mean_rank_variance = sum(rank_variances) / len(rank_variances)
    correlation_coefficient = (sum((d - mean_degree) * (r - mean_rank_variance) for d, r in zip(degrees, rank_variances)) /
                                math.sqrt(sum((d - mean_degree) ** 2 for d in degrees) *
                                          sum((r - mean_rank_variance) ** 2 for r in rank_variances)))
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(degrees),
        "n_max": max(len(instance) for instance in [generate_sat_instance(n) for n in range(5, 41)]),
        "conjecture_holds": abs(correlation_coefficient) <= 0.2,
        "counterexample": "" if abs(correlation_coefficient) <= 0.2 else "High correlation coefficient"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all("metric_value" in result and result["metric_value"] is not None for result in results):
        mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
        std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
        elif any(result["counterexample"] != "" for result in results):
            first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["counterexample"] != "")
            print(f"RESULT: FALSIFIED counterexample=\"{next(result['counterexample'] for result in results if result['counterexample'] != '')}\" first_failing_seed={first_failing_seed}")
        else:
            print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")
    else:
        print("RESULT: INCONCLUSIVE metric_value missing or None")
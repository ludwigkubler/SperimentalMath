# auto-injected by SEC sandbox
import math
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from itertools import combinations

def generate_dnf(n, m):
    clauses = []
    for _ in range(m):
        variables = random.sample(range(n), random.randint(1, n))
        clause = [(-1 if random.choice([True, False]) else 1) * var for var in variables]
        clauses.append(clause)
    return clauses

def lex_maximal_shifted_hypergraph(hypergraph):
    shifted_edges = set()
    for edge in hypergraph:
        for i in range(len(edge)):
            new_edge = tuple(sorted(edge[:i] + (edge[i] * -1,) + edge[i+1:]))
            if new_edge not in shifted_edges:
                shifted_edges.add(new_edge)
    return shifted_edges

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m_max = n**2
        for _ in range(5):  # Ensure at least 30 instances per seed
            m = random.randint(1, m_max)
            dnf = generate_dnf(n, m)
            
            hypergraph = set()
            for clause in dnf:
                hypergraph.update(combinations(range(n), len(clause)))
            
            shifted_edges = lex_maximal_shifted_hypergraph(hypergraph)
            num_edges = len(shifted_edges)
            
            if n == 2:  # k-CLIQUE case
                k = m
                expected_min_edges = n**0.5 - 2 * (k**0.5)
                if num_edges < expected_min_edges:
                    return {
                        "metric_name": "E_shifted",
                        "metric_value": num_edges,
                        "instances_tested": len(n_values),
                        "conjecture_holds": False,
                        "counterexample": f"k-CLIQUE instance with n={n}, m={m} failed, expected at least {expected_min_edges:.2f} edges but got {num_edges}"
                    }
            else:
                expected_max_edges = 0
                for i in range(1, n+1):
                    expected_max_edges += (i * (n - i))
                if num_edges > expected_max_edges + 2 * (m**0.5):
                    return {
                        "metric_name": "E_shifted",
                        "metric_value": num_edges,
                        "instances_tested": len(n_values),
                        "conjecture_holds": False,
                        "counterexample": f"General DNF instance with n={n}, m={m} failed, expected at most {expected_max_edges + 2 * (m**0.5):.2f} edges but got {num_edges}"
                    }
    
    return {
        "metric_name": "E_shifted",
        "metric_value": sum(results) / len(results),
        "instances_tested": len(n_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean = sum(results) / len(results)
    std_dev = (sum((x - mean)**2 for x in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r <= log(len(seeds)) + 2 * (len(results)**0.5)) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean:.2f} std={std_dev:.2f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if r > log(len(seeds)) + 2 * (len(results)**0.5))
        print(f"RESULT: FALSIFIED counterexample=\"General DNF instance\" first_failing_seed={first_failing_seed}")
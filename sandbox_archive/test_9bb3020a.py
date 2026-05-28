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
    
    def generate_random_graph(n):
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    edges.add((i, j))
        return edges
    
    def compute_quandle_rank(graph):
        n = len(graph)
        rank = 0
        while True:
            found_new_element = False
            for i in range(n):
                for j in range(i + 1, n):
                    if (i, j) not in graph and (j, i) not in graph:
                        new_element = set()
                        for k in range(n):
                            if (k, i) in graph and (k, j) not in graph:
                                new_element.add((k, j))
                            elif (k, i) not in graph and (k, j) in graph:
                                new_element.add((k, i))
                        if len(new_element) > 0:
                            found_new_element = True
                            rank += 1
                            graph.update(new_element)
            if not found_new_element:
                break
        return rank
    
    def generate_tseitin_formula(graph):
        n = len(graph)
        literals = {i: f"x{i}" for i in range(n)}
        clauses = []
        for (i, j) in graph:
            clauses.append([literals[i], literals[j]])
            clauses.append([-literals[i], -literals[j]])
            clauses.append([-literals[i], literals[j]])
            clauses.append([literals[i], -literals[j]])
        return clauses
    
    def resolution_refutation_length(clauses):
        stack = []
        while True:
            unit_clause = next((c for c in clauses if len(c) == 1), None)
            if not unit_clause:
                break
            literal = unit_clause[0]
            clauses.remove(unit_clause)
            for clause in clauses[:]:
                if literal in clause:
                    clauses.remove(clause)
                elif -literal in clause:
                    index = clause.index(-literal)
                    clause.pop(index)
                    clause.extend([l for l in unit_clause if l != literal])
                    stack.append(clause)
        return len(stack)
    
    n = random.randint(5, 40)
    graph = generate_random_graph(n)
    quandle_rank = compute_quandle_rank(graph)
    tseitin_formula = generate_tseitin_formula(graph)
    refutation_length = resolution_refutation_length(tseitin_formula)
    
    return {
        "metric_name": "resolution_refutation_length",
        "metric_value": refutation_length,
        "instances_tested": 1,
        "conjecture_holds": refutation_length >= 2 ** quandle_rank,
        "counterexample": f"quandle_rank={quandle_rank}, refutation_length={refutation_length}" if not conjecture_holds else ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r >= 2 ** quandle_rank) / len(results)
    
    if support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(r < 2 ** quandle_rank for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result < 2 ** quandle_rank)
        print(f"RESULT: FALSIFIED counterexample='quandle_rank={quandle_rank}, refutation_length<{2**quandle_rank}' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")
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

def generate_random_sat_instance(n):
    variables = set()
    clauses = []
    for _ in range(n):
        clause = [random.choice([1, -1]) * (i + 1) for i in range(random.randint(2, n))]
        variables.update(abs(x) for x in clause)
        clauses.append(clause)
    return list(variables), clauses

def dpll_solve(instance, assignment):
    variables, clauses = instance
    free_variables = [v for v in variables if v not in assignment]
    if not free_variables:
        unsatisfiable = any(all(assignment.get(v, False) == (c > 0)) or all(assignment.get(v, False) == (c < 0)) for c in clauses)
        return not unsatisfiable
    v = free_variables[0]
    assignment[v] = True
    if dpll_solve(instance, assignment):
        return True
    del assignment[v]
    assignment[v] = False
    return dpll_solve(instance, assignment)

def construct_tree_like_resolution_proof(instance):
    variables, clauses = instance
    proof = []
    for v in variables:
        unit_clause = next((c for c in clauses if len(c) == 1 and abs(c[0]) == v), None)
        if unit_clause:
            proof.append(unit_clause)
            clauses.remove(unit_clause)
        else:
            clause = random.choice(clauses)
            proof.append(clause)
            clauses.remove(clause)
    return proof

def extract_coxeter_dynkin_diagram(proof):
    diagram = {}
    for clause in proof:
        for literal in clause:
            if abs(literal) not in diagram:
                diagram[abs(literal)] = set()
            for other_literal in clause:
                if abs(other_literal) != abs(literal):
                    diagram[abs(literal)].add(abs(other_literal))
    return diagram

def count_vertices_in_diagram(diagram):
    return sum(len(neighbors) for neighbors in diagram.values())

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        total_vertices = 0
        
        while instances_tested < 30:
            instance = generate_random_sat_instance(n)
            if dpll_solve(instance, {}):
                proof = construct_tree_like_resolution_proof(instance)
                diagram = extract_coxeter_dynkin_diagram(proof)
                vertices = count_vertices_in_diagram(diagram)
                total_vertices += vertices
                instances_tested += 1
        
        mean_vertices = total_vertices / instances_tested
        upper_bound = n**2 * math.log(n)
        
        results.append({
            "n": n,
            "mean_vertices": mean_vertices,
            "upper_bound": upper_bound,
            "conjecture_holds": mean_vertices <= upper_bound
        })
    
    metric_value = sum(res["mean_vertices"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    return {
        "metric_name": "Mean vertices in Coxeter-Dynkin diagram",
        "metric_value": metric_value,
        "instances_tested": 30 * len(n_values),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else f"Mean vertices {metric_value} > upper bound {upper_bound}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=NA support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mean vertices > upper bound' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")
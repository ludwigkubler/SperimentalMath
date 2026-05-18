# auto-injected by SEC sandbox
import json
import os
import time
import re
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import itertools
from collections import deque

def generate_3_regular_graph(n, seed):
    random.seed(seed)
    while True:
        # Create a list of vertices
        vertices = list(range(n))
        # Create a list of edges
        edges = []
        # Create a degree dictionary
        degrees = {v: 0 for v in vertices}
        # Create a list of stubs
        stubs = []
        for v in vertices:
            stubs.extend([v] * 3)
        # Shuffle the stubs
        random.shuffle(stubs)
        # Pair the stubs to form edges
        for i in range(0, len(stubs), 2):
            u, v = stubs[i], stubs[i+1]
            if u != v and (u, v) not in edges and (v, u) not in edges:
                edges.append((u, v))
                degrees[u] += 1
                degrees[v] += 1
        # Check if the graph is simple and 3-regular
        if len(edges) == 3 * n // 2 and all(d == 3 for d in degrees.values()):
            # Check if the graph is connected
            visited = set()
            queue = deque([vertices[0]])
            while queue:
                v = queue.popleft()
                if v not in visited:
                    visited.add(v)
                    for u, w in edges:
                        if u == v and w not in visited:
                            queue.append(w)
                        elif w == v and u not in visited:
                            queue.append(u)
            if len(visited) == n:
                return vertices, edges

def generate_odd_charge(n, edges, seed):
    random.seed(seed)
    # Create a list of vertices
    vertices = list(range(n))
    # Create a charge dictionary
    charge = {v: 0 for v in vertices}
    # Assign random charges to vertices
    for v in vertices:
        charge[v] = random.randint(0, 1)
    # Ensure the sum of charges is odd
    if sum(charge.values()) % 2 == 0:
        charge[random.choice(vertices)] = 1 - charge[random.choice(vertices)]
    return charge

def bfs_gauge(vertices, edges, charge, root):
    # Create a gauge dictionary
    gauge = {e: 0 for e in edges}
    # Create a visited dictionary
    visited = {v: False for v in vertices}
    # Create a queue
    queue = deque([root])
    # Mark the root as visited
    visited[root] = True
    # Perform BFS
    while queue:
        v = queue.popleft()
        for u, w in edges:
            if u == v and not visited[w]:
                # Calculate the gauge for the edge
                gauge[(u, w)] = (charge[w] + sum(gauge[(w, x)] for x, y in edges if y == w)) % 2
                # Mark the vertex as visited
                visited[w] = True
                # Add the vertex to the queue
                queue.append(w)
            elif w == v and not visited[u]:
                # Calculate the gauge for the edge
                gauge[(w, u)] = (charge[u] + sum(gauge[(u, x)] for x, y in edges if y == u)) % 2
                # Mark the vertex as visited
                visited[u] = True
                # Add the vertex to the queue
                queue.append(u)
    return gauge

def matrix_multiply(A, B):
    # Create a result matrix
    result = [[0 for _ in range(len(B[0]))] for _ in range(len(A))]
    # Perform matrix multiplication
    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(B)):
                result[i][j] += A[i][k] * B[k][j]
    return result

def matrix_subtract(A, B):
    # Create a result matrix
    result = [[0 for _ in range(len(A[0]))] for _ in range(len(A))]
    # Perform matrix subtraction
    for i in range(len(A)):
        for j in range(len(A[0])):
            result[i][j] = A[i][j] - B[i][j]
    return result

def matrix_transpose(A):
    # Create a result matrix
    result = [[0 for _ in range(len(A))] for _ in range(len(A[0]))]
    # Perform matrix transposition
    for i in range(len(A)):
        for j in range(len(A[0])):
            result[j][i] = A[i][j]
    return result

def matrix_power_iteration(A, max_iter=100, tol=1e-6):
    # Initialize a random vector
    b = [random.random() for _ in range(len(A))]
    # Normalize the vector
    norm = math.sqrt(sum(x**2 for x in b))
    b = [x / norm for x in b]
    # Perform power iteration
    for _ in range(max_iter):
        # Multiply the matrix by the vector
        b_new = [sum(A[i][j] * b[j] for j in range(len(b))) for i in range(len(A))]
        # Normalize the vector
        norm = math.sqrt(sum(x**2 for x in b_new))
        b_new = [x / norm for x in b_new]
        # Check for convergence
        if sum((b_new[i] - b[i])**2 for i in range(len(b))) < tol:
            break
        b = b_new
    # Calculate the eigenvalue
    eigenvalue = sum(A[i][j] * b[j] for i in range(len(A)) for j in range(len(b))) / sum(b[i]**2 for i in range(len(b)))
    return eigenvalue

def compute_mu(vertices, edges, gauge):
    # Create the signed adjacency matrix
    A = [[0 for _ in range(len(vertices))] for _ in range(len(vertices))]
    for u, v in edges:
        sigma = (-1) ** gauge[(u, v)]
        A[u][v] = sigma
        A[v][u] = sigma
    # Create the degree matrix
    D = [[0 for _ in range(len(vertices))] for _ in range(len(vertices))]
    for i in range(len(vertices)):
        D[i][i] = sum(abs(A[i][j]) for j in range(len(vertices)))
    # Create the signed Laplacian matrix
    L = matrix_subtract(D, A)
    # Compute the smallest eigenvalue
    mu = matrix_power_iteration(L)
    return mu

def compute_t_star(vertices, edges, charge, gauge):
    # Create a list of clauses
    clauses = []
    for v in vertices:
        clause = []
        for u, w in edges:
            if u == v or w == v:
                clause.append((u, w))
        clauses.append(clause)
    # Create a list of variables
    variables = list(range(len(edges)))
    # Create a list of assignments
    assignments = []
    # Perform DPLL with unit propagation and dynamic variable ordering
    def dpll(clauses, variables, assignments):
        # Check if all clauses are satisfied
        if all(any((u, v) in assignments or (-u, -v) in assignments for u, v in clause) for clause in clauses):
            return len(assignments)
        # Check if any clause is unsatisfied
        if any(all((u, v) not in assignments and (-u, -v) not in assignments for u, v in clause) for clause in clauses):
            return float('inf')
        # Select the next variable to assign
        variable = variables[0]
        # Try assigning the variable to true
        assignments.append((variable,))
        t_true = dpll(clauses, variables[1:], assignments)
        assignments.pop()
        # Try assigning the variable to false
        assignments.append((-variable,))
        t_false = dpll(clauses, variables[1:], assignments)
        assignments.pop()
        # Return the minimum number of assignments
        return min(t_true, t_false)
    # Compute the minimum number of assignments
    t_star = dpll(clauses, variables, assignments)
    return t_star

def run_trial(seed):
    # Set the random seed
    random.seed(seed)
    # Initialize the results
    results = {
        "metric_name": "log_2 t* / (mu * |V|)",
        "metric_value": 0.0,
        "instances_tested": 0,
        "conjecture_holds": True,
        "counterexample": ""
    }
    # Sweep over the graph sizes
    for n in [8, 10, 12, 14, 16, 18, 20]:
        # Generate a 3-regular graph
        vertices, edges = generate_3_regular_graph(n, seed)
        # Generate an odd charge
        charge = generate_odd_charge(n, edges, seed)
        # Build the BFS gauge
        gauge = bfs_gauge(vertices, edges, charge, vertices[0])
        # Compute the signed Laplacian eigenvalue
        mu = compute_mu(vertices, edges, gauge)
        # Compute the minimum number of assignments
        t_star = compute_t_star(vertices, edges, charge, gauge)
        # Update the results
        results["instances_tested"] += 1
        if t_star == float('inf'):
            results["conjecture_holds"] = False
            results["counterexample"] = f"Graph with n={n} is unsatisfiable"
            break
        metric_value = math.log2(t_star) / (mu * n)
        results["metric_value"] += metric_value
        if metric_value < 0.05:
            results["conjecture_holds"] = False
            results["counterexample"] = f"Graph with n={n}, mu={mu}, t*={t_star} violates the conjecture"
            break
    # Compute the average metric value
    results["metric_value"] /= results["instances_tested"]
    return results

if __name__ == "__main__":
    # Read the seeds from the command line
    seeds = sys.argv[1:] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    # Initialize the results
    total_metric_value = 0.0
    total_instances_tested = 0
    total_support = 0
    counterexample = ""
    # Run the trials
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        total_metric_value += result["metric_value"]
        total_instances_tested += result["instances_tested"]
        if result["conjecture_holds"]:
            total_support += 1
        if not result["conjecture_holds"] and not counterexample:
            counterexample = result["counterexample"]
    # Compute the mean and standard deviation of the metric value
    mean_metric_value = total_metric_value / len(seeds)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(seeds))
    # Compute the fraction of seeds that support the conjecture
    support_fraction = total_support / len(seeds)
    # Print the final result
    if counterexample:
        print(f'RESULT: FALSIFIED counterexample="{counterexample}" first_failing_seed={seeds[total_support]}')
    elif support_fraction >= 0.8:
        print(f'RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}')
    else:
        print('RESULT: INCONCLUSIVE reason=insufficient_support')
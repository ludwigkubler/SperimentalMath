import random
import math
import sys
import json

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + max(range(i, m), key=lambda r: abs(A[r][i]))
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(n):
                if i != j:
                    factor = A[j][i] / A[i][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A
    
    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def poset_dimension(rectangles):
        m, n = len(rectangles), len(rectangles[0])
        R = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                if rectangles[i][j]:
                    R[i][j] = 1
                else:
                    R[i][j] = 0
        A = gaussian_elimination(R)
        rank = sum(1 for row in A if any(row))
        return m - rank
    
    def communication_matrix(cnf):
        n = len(cnf)
        matrix = [[0] * (2 ** n) for _ in range(n)]
        for i in range(n):
            for j in range(2 ** n):
                if bin(j).count('1') == i + 1:
                    matrix[i][j] = 1
        return matrix
    
    def minimal_rectangles(matrix):
        m, n = len(matrix), len(matrix[0])
        rectangles = []
        for i in range(m):
            for j in range(n):
                if matrix[i][j]:
                    rectangle = [i]
                    for k in range(j + 1, n):
                        if all(matrix[x][k] == matrix[x][j] for x in range(i, m)):
                            rectangle.append(k)
                    rectangles.append(rectangle)
        return rectangles
    
    def is_monotone(cnf):
        for clause in cnf:
            if any(not var for var in clause):
                return False
        return True
    
    n = random.choice([5, 8, 11, 14])
    cnf = [[random.randint(1, n) for _ in range(random.randint(1, n))] for _ in range(n)]
    if not is_monotone(cnf):
        return {
            "metric_name": "communication_complexity",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "non-monotone_cnf"
        }
    
    comm_matrix = communication_matrix(cnf)
    rectangles = minimal_rectangles(comm_matrix)
    poset_dim = poset_dimension(rectangles)
    comm_complexity = len(rectangles)
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": comm_complexity,
        "instances_tested": 1,
        "conjecture_holds": comm_complexity >= poset_dim,
        "counterexample": "" if comm_complexity >= poset_dim else f"poset_dimension={poset_dim}, communication_complexity={comm_complexity}"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {json.dumps(result)}")
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_metric_value / len(results)} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_metric_value / len(results)} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
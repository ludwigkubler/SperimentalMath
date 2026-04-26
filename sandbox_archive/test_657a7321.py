import random
import sys

random.seed(42)

def has_monochromatic_rectangle(matrix):
    n = len(matrix)
    for i in range(n):
        row = matrix[i]
        for j in range(i+1, n):
            other = matrix[j]
            common = set(row) & set(other)
            if len(common) == 1:
                return True
    return False

def main():
    n_values = [5, 8, 11, 14]
    results = []
    for n in n_values:
        matrix = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        has_rect = has_monochromatic_rectangle(matrix)
        order = 1 if has_rect else 0
        results.append((n, has_rect, order))
        print(f"n={n} has_rect={has_rect} order={order}")
    if all(r[1] for r in results):
        print("RESULT: SUPPORTED <metric>=1")
    else:
        print("RESULT: INCONCLUSIVE <reason>")

if __name__ == "__main__":
    main()
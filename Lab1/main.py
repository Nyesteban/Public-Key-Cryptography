import timeit


# Euclidean algorithm
def gcd_euclidean(a, b):
    while b:
        a, b = b, a % b
    return a


# Dijkstra's algorithm
def gcd_dijkstra(a, b):
    if a == 0:
        return b
    elif b == 0:
        return a
    elif a == b:
        return a
    elif a > b:
        return gcd_dijkstra(a - b, b)
    else:
        return gcd_dijkstra(a, b - a)


# Bishop's algorithm
def gcd_bishop(a, b):
    if a == 0:
        return b
    elif b == 0:
        return a
    while a != b:
        if a > b:
            a = a - b
        else:
            a, b = b, a
    return a


# Test Euclidean algorithm
def euclidean_test(a, b):
    print("Euclidean: " + str(a) + ", " + str(b))
    print("Solution: " + str(gcd_euclidean(a, b)))
    print("Time elapsed in ms: " + str(timeit.timeit(lambda: gcd_euclidean(a, b), number=1000) * 1000))
    print('\n')


# Test Dijkstra's algorithm
def dijkstra_test(a, b):
    print("Dijkstra: " + str(a) + ", " + str(b))
    print("Solution: " + str(gcd_dijkstra(a, b)))
    print("Time elapsed in ms: " + str(timeit.timeit(lambda: gcd_dijkstra(a, b), number=1000) * 1000))
    print('\n')


# Test Bishop algorithm
def bishop_test(a, b):
    print("Bishop: " + str(a) + ", " + str(b))
    print("Solution: " + str(gcd_bishop(a, b)))
    print("Time elapsed in ms: " + str(timeit.timeit(lambda: gcd_bishop(a, b), number=1000) * 1000))
    print('\n')


if __name__ == '__main__':
    # Tests and running time analysis
    # Format is algorithm type: values; solution; time

    euclidean_test(10, 15)
    dijkstra_test(10, 15)
    bishop_test(10, 15)

    euclidean_test(42, 56)
    dijkstra_test(42, 56)
    bishop_test(42, 56)

    euclidean_test(461952, 116298)
    dijkstra_test(461952, 116298)
    bishop_test(461952, 116298)

    euclidean_test(7966496, 314080416)
    dijkstra_test(7966496, 314080416)
    bishop_test(7966496, 314080416)

    euclidean_test(24826148, 45296490)
    dijkstra_test(24826148, 45296490)
    bishop_test(24826148, 45296490)

    euclidean_test(0, 0)
    dijkstra_test(0, 0)
    bishop_test(0, 0)

    euclidean_test(10, 0)
    dijkstra_test(10, 0)
    bishop_test(10, 0)

    euclidean_test(0, 100)
    dijkstra_test(0, 100)
    bishop_test(0, 100)

    euclidean_test(768454923, 542167814)
    dijkstra_test(768454923, 542167814)
    bishop_test(768454923, 542167814)

    euclidean_test(768, 542)
    dijkstra_test(768, 542)
    bishop_test(768, 542)

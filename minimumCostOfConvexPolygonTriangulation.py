from math import sqrt


class calculateMinimum:
    def __init__(self):
        self.point1 = []
        self.point2 = []
        self.point3 = []

    def dist(self, pointA, pointB):
        dist = sqrt((pointB[0] - pointA[0]) ** 2 + (pointB[1] - pointA[1]) ** 2)
        return dist

    def cost(self, points, i, j, k, n):
        p1, p2, p3 = points[i], points[j], points[k]
        # if i == 0 and j == n - 1:
        #     self.point1 = p1
        #     self.point2 = p2
        #     self.point3 = p3
        return self.dist(p1, p2) + self.dist(p2, p3) + self.dist(p3, p1)

    def mTCDP(self, points, n):

        if n < 3:
            return 0, [], [], []

        matrix = [[0 for i in range(n)] for j in range(n)]

        for gap in range(0, n):
            i = 0
            for j in range(gap, n):
                if j < i + 2:
                    matrix[i][j] = 0
                else:
                    matrix[i][j] = float("Inf")
                    for k in range(i + 1, j):
                        val = (
                            matrix[i][k] + matrix[k][j] + self.cost(points, i, j, k, n)
                        )
                        if matrix[i][j] > val:
                            if i == 0 and j == n - 1:
                                self.point1, self.point2, self.point3 = (
                                    points[i],
                                    points[j],
                                    points[k],
                                )
                            matrix[i][j] = val
                i += 1

        return matrix[0][n - 1], self.point1, self.point2, self.point3


if __name__ == "__main__":
    points = [[0, 0], [1, 0], [2, 1], [1, 2], [0, 2]]
    n = len(points)

    min = calculateMinimum().mTCDP(points, n)
    print(min)

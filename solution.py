#!/usr/bin/python3

from collections import deque
import inspect
import time
from typing import List
from typing import Set

class Solution1_DFS:
    __NEIGHBORS: List[List[int]] = [[1, 0], [0, 1], [-1, 0], [0, -1]]

    #
    # Depth first search for an island, and its corresponding area, 
    # given starting coordinates.
    #
    # Time = O(n + 4**n) => O(4**n)
    #        n = number of cells in grid (nodes in graph)
    #
    # Space = O(n + 1 + n) => O(2n+1) => O(n)  [for call stack]
    #         Call stack is n + 1.
    #         Visited set is n.
    #
    def findIslandAreaDFS(self, grid: List[List[int]], x: int, y: int, visited: Set) -> int:
        outOfBounds: bool = 0 > x or 0 > y or len(grid) <= y or len(grid[y]) <= x
        if outOfBounds: return 0

        inWater: bool = 0 == grid[y][x]
        if inWater: return 0

        alreadyVisited: bool = (x, y) in visited
        if alreadyVisited: return 0

        visited.add((x, y))
        
        area: int = 1
        for neighbor in self.__NEIGHBORS:
            area += self.findIslandAreaDFS(grid, x + neighbor[0], y + neighbor[1], visited)

        return area
    
    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        area = 0
        visited = set()
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                if not (x, y) in visited: # Optimization
                    area = max(area, self.findIslandAreaDFS(grid, x, y, visited))
        return area

class Solution2_DFS:
    __NEIGHBORS: List[List[int]] = [[1, 0], [0, 1], [-1, 0], [0, -1]]

    #
    # Depth first search for an island, and its corresponding area, 
    # given starting coordinates.
    #
    # Time = O(n + 4**n) => O(4**n)
    #        n = number of cells in grid (nodes in graph)
    #
    # Space = O(n + 1 + n) => O(2n+1) => O(n)  [for call stack]
    #         Call stack is n + 1.
    #         Visited set is n.
    #
    def findIslandAreaDFS(self, grid: List[List[int]], x: int, y: int, visited: list) -> int:
        outOfBounds: bool = 0 > x or 0 > y or len(grid) <= y or len(grid[y]) <= x
        if outOfBounds: return 0

        inWater: bool = 0 == grid[y][x]
        if inWater: return 0

        alreadyVisited: bool = 0 != visited[y * len(grid[0]) + x]
        if alreadyVisited: return 0

        visited[y * len(grid[0]) + x] = 1
        
        area: int = 1
        for neighbor in self.__NEIGHBORS:
            area += self.findIslandAreaDFS(grid, x + neighbor[0], y + neighbor[1], visited)

        return area
    
    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        area = 0
        visited = [0] * len(grid) * len(grid[0])
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                if 0 == visited[y * len(grid[0]) + 1]: # Optimization
                    area = max(area, self.findIslandAreaDFS(grid, x, y, visited))
        return area

class Solution3_DFS:
    #
    # Depth first search for an island, and its corresponding area, 
    # given starting coordinates.
    #
    # Time = O(n + 4**n) => O(4**n)
    #        n = number of cells in grid (nodes in graph)
    #
    # Space = O(n + 1 + n) => O(2n+1) => O(n)  [for call stack]
    #         Call stack is n + 1.
    #         Visited set is n.
    #
    def findIslandAreaDFS(self, grid: List[List[int]], x: int, y: int) -> int:
        if 0 > x or 0 > y or len(grid) <= y or len(grid[y]) <= x \
           or 0 == grid[y][x]:
            return 0

        grid[y][x] = 0 # Mark node visited.
        
        # The following four calls are faster outside of a loop.
        area: int = 1
        area += self.findIslandAreaDFS(grid, x + 1, y + 0)
        area += self.findIslandAreaDFS(grid, x + 0, y + 1)
        area += self.findIslandAreaDFS(grid, x - 1, y + 0)
        area += self.findIslandAreaDFS(grid, x + 0, y - 1)

        return area
    
    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        area = 0
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                if 0 != grid[y][x]: # Optimization
                    area = max(area, self.findIslandAreaDFS(grid, x, y))
        return area

class Solution1_BFS:
    __NEIGHBORS: List[List[int]] = [[1, 0], [0, 1], [-1, 0], [0, -1]]

    #
    # Depth first search for an island, and its corresponding area, 
    # given starting coordinates.
    #
    # Time = O(n + 4*n) => O(4*n)
    #        n = number of cells in grid (nodes in graph)
    #
    # Space = O(n)
    #         Visited set is n.
    #
    def findIslandAreaBFS(self, grid: List[List[int]], x: int, y: int, visited: Set) -> int:
        area = 0 if 0 == grid[y][x] else 1
        
        q = deque()
        q.append((x, y))
        visited.add((x, y))
        while 0 < len(q):
            for count in range(len(q), 0, -1):
                x, y = q.pop()
                for dx, dy in self.__NEIGHBORS:
                    nx, ny = x + dx, y + dy # Neighbors
                    if 0 <= nx and 0 <= ny and len(grid) > ny and len(grid[ny]) > nx \
                       and 0 != grid[ny][nx] \
                       and not (nx, ny) in visited:
                        area += 1
                        q.append((nx, ny))
                        visited.add((nx, ny))

        return area
    
    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        area = 0
        visited = set()
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                if 0 != grid[y][x] \
                   and not (x, y) in visited: # Optimization
                    area = max(area, self.findIslandAreaBFS(grid, x, y, visited))
        return area

class Solution2_BFS:
    #
    # Depth first search for an island, and its corresponding area, 
    # given starting coordinates.
    #
    # Time = O(n + 4*n) => O(4*n)
    #        n = number of cells in grid (nodes in graph)
    #
    # Space = O(n)
    #         Visited set is n.
    #
    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        area = 0
        q = deque()
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                if 0 != grid[y][x]:
                    assert(0 != grid[y][x])
                    islandArea = 1
                    
                    assert(0 == len(q))
                    q.append((x, y))
                    grid[y][x] = 0
                    while 0 < len(q):
                        for count in range(len(q), 0, -1):
                            ox, oy = q.pop()

                            # The following four blocks are faster outside of a loop.

                            nx, ny = ox + 1, oy + 0
                            if 0 <= nx and 0 <= ny and len(grid) > ny and len(grid[ny]) > nx and 0 != grid[ny][nx]:
                                islandArea += 1
                                q.append((nx, ny))
                                grid[ny][nx] = 0

                            nx, ny = ox + 0, oy + 1
                            if 0 <= nx and 0 <= ny and len(grid) > ny and len(grid[ny]) > nx and 0 != grid[ny][nx]:
                                islandArea += 1
                                q.append((nx, ny))
                                grid[ny][nx] = 0

                            nx, ny = ox - 1, oy + 0
                            if 0 <= nx and 0 <= ny and len(grid) > ny and len(grid[ny]) > nx and 0 != grid[ny][nx]:
                                islandArea += 1
                                q.append((nx, ny))
                                grid[ny][nx] = 0

                            nx, ny = ox + 0, oy - 1
                            if 0 <= nx and 0 <= ny and len(grid) > ny and len(grid[ny]) > nx and 0 != grid[ny][nx]:
                                islandArea += 1
                                q.append((nx, ny))
                                grid[ny][nx] = 0
                    
                    area = max(area, islandArea)
        return area

def test1(solution):
    grid = [[0,0,1,0,0,0,0,1,0,0,0,0,0],[0,0,0,0,0,0,0,1,1,1,0,0,0],[0,1,1,0,1,0,0,0,0,0,0,0,0],[0,1,0,0,1,1,0,0,1,0,1,0,0],[0,1,0,0,1,1,0,0,1,1,1,0,0],[0,0,0,0,0,0,0,0,0,0,1,0,0],[0,0,0,0,0,0,0,1,1,1,0,0,0],[0,0,0,0,0,0,0,1,1,0,0,0,0]]
    expected = 6
    startTime = time.time()
    result = solution.maxAreaOfIsland(grid)
    endTime = time.time()
    print("{}:{}({:.6f} sec) result = {}".format(inspect.currentframe().f_code.co_name, type(solution), endTime - startTime, result))
    assert(expected == result)

def test2(solution):
    grid = [[0,0,0,0,0,0,0,0]]
    expected = 0
    startTime = time.time()
    result = solution.maxAreaOfIsland(grid)
    endTime = time.time()
    print("{}:{}({:.6f} sec) result = {}".format(inspect.currentframe().f_code.co_name, type(solution), endTime - startTime, result))
    assert(expected == result)

if "__main__" == __name__:
    test1(Solution1_DFS())
    test1(Solution2_DFS())
    test1(Solution3_DFS())
    test1(Solution1_BFS())
    test2(Solution2_BFS())

    test2(Solution1_DFS())
    test2(Solution2_DFS())
    test2(Solution3_DFS())
    test2(Solution1_BFS())
    test2(Solution2_BFS())

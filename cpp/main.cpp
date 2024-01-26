/*!
    \file "main.cpp"

    Author: Matt Ervin <matt@impsoftware.org>
    Formatting: 4 spaces/tab (spaces only; no tabs), 120 columns.
    Doc-tool: Doxygen (http://www.doxygen.com/)

    https://leetcode.com/problems/max-area-of-island/
*/

//!\sa https://github.com/doctest/doctest/blob/master/doc/markdown/main.md
#define DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN

#include "utils.hpp"

class Solution1_DFS {
public:
    /*
        Depth first search for an island, given starting coordinates.
     
        Time = O(n + 4**n) => O(4**n)
               n = number of cells in grid (nodes in graph)
     
        Space = O(n + 1 + n) => O(2n+1) => O(n)  [for call stack]
                Call stack is n + 1.
                Visited set is n.
    */
    int findIslandAreaDFS(vector<vector<int>>& grid, size_t x, size_t y) const {
        int area{};

        auto const inRange = 0 <= x && 0 <= y && grid.size() > y && grid[y].size() > x;
        if (inRange) {
            auto const isLand = 0 != grid[y][x];
            if (isLand) {
                grid[y][x] = 0;
                area = 1;
                area += findIslandAreaDFS(grid, x + 1, y + 0);
                area += findIslandAreaDFS(grid, x + 0, y + 1);
                area += findIslandAreaDFS(grid, x - 1, y + 0);
                area += findIslandAreaDFS(grid, x + 0, y - 1);
            }
        }
        
        return area;
    }
    
    int maxAreaOfIsland(vector<vector<int>>& grid) {
        int area = 0;

        for (size_t y = 0; grid.size() > y; ++y) {
            for (size_t x = 0; grid[y].size() > x; ++x) {
                if (0 != grid[y][x]) {
                    area = (std::max)(area, findIslandAreaDFS(grid, x, y));
                }
            }
        }

        return area;
    }
};

class Solution1_BFS {
    static constexpr const std::array<std::tuple<ssize_t, ssize_t>, 4> neighbors_ = {
        std::make_tuple(1, 0), std::make_tuple(0, 1), std::make_tuple(-1, 0), std::make_tuple(0, -1)
    };
    std::deque<std::tuple<size_t, size_t>> que_{};
public:
    /*
        Depth first search for an island.
        
        Time = O(n + 4*n) => O(4*n)
               n = number of cells in grid (nodes in graph)
        
        Space = O(n/2) => O(n)
                Queue contains up to n/2 items.
    */
    int maxAreaOfIsland(vector<vector<int>>& grid) {
        int area = 0;

        for (size_t gy = 0; grid.size() > gy; ++gy) {
            for (size_t gx = 0; grid[gy].size() > gx; ++gx) {
                if (0 != grid[gy][gx]) {
                    assert(que_.empty());
                    grid[gy][gx] = 0;
                    que_.push_back(std::make_tuple(gx, gy));
                    int islandArea = 1;
                    while (!que_.empty()) {
                        for (auto _ = que_.size(); _; --_) {
                            auto [ox, oy] = que_.front(); // Original (x, y).
                            que_.pop_front();

                            for (auto [dx, dy] : neighbors_) {
                                auto const nx = ox + dx; // New x.
                                auto const ny = oy + dy; // New y.
                                auto const inRange = 0 <= nx && 0 <= ny && grid.size() > ny && grid[ny].size() > nx;
                                if (inRange) {
                                    auto const isLand = 0 != grid[ny][nx];
                                    if (isLand) {
                                        grid[ny][nx] = 0;
                                        que_.push_back(std::make_tuple(nx, ny));
                                        ++islandArea;
                                    }
                                }
                            }
                        }
                    }

                    area = (std::max)(area, islandArea);
                }
            }
        }

        return area;
    }
};

// [----------------(120 columns)---------------> Module Code Delimiter <---------------(120 columns)----------------]

namespace doctest {
    const char* testName() noexcept { return doctest::detail::g_cs->currentTest->m_name; }
} // namespace doctest {

TEST_CASE("Case 1")
{
    cerr << doctest::testName() << '\n';
    auto grid = vector<vector<int>>{
        {0,0,1,0,0,0,0,1,0,0,0,0,0},
        {0,0,0,0,0,0,0,1,1,1,0,0,0},
        {0,1,1,0,1,0,0,0,0,0,0,0,0},
        {0,1,0,0,1,1,0,0,1,0,1,0,0},
        {0,1,0,0,1,1,0,0,1,1,1,0,0},
        {0,0,0,0,0,0,0,0,0,0,1,0,0},
        {0,0,0,0,0,0,0,1,1,1,0,0,0},
        {0,0,0,0,0,0,0,1,1,0,0,0,0}
    };
    int expected = 6;
    auto solution = Solution1_DFS{};
    { // New scope.
        auto const start = std::chrono::steady_clock::now();
        auto const result = solution.maxAreaOfIsland(grid);
        CHECK(expected == result);
        cerr << "Elapsed time: " << elapsed_time_t{start} << '\n';
    }
    cerr << "\n";
}

TEST_CASE("Case 2")
{
    cerr << doctest::testName() << '\n';
    auto grid = vector<vector<int>>{
        {0,0,0,0,0,0,0,0},
    };
    int expected = 0;
    auto solution = Solution1_DFS{};
    { // New scope.
        auto const start = std::chrono::steady_clock::now();
        auto const result = solution.maxAreaOfIsland(grid);
        CHECK(expected == result);
        cerr << "Elapsed time: " << elapsed_time_t{start} << '\n';
    }
    cerr << "\n";
}

TEST_CASE("Case 10")
{
    cerr << doctest::testName() << '\n';
    auto grid = vector<vector<int>>{
        {0,0,1,0,0,0,0,1,0,0,0,0,0},
        {0,0,0,0,0,0,0,1,1,1,0,0,0},
        {0,1,1,0,1,0,0,0,0,0,0,0,0},
        {0,1,0,0,1,1,0,0,1,0,1,0,0},
        {0,1,0,0,1,1,0,0,1,1,1,0,0},
        {0,0,0,0,0,0,0,0,0,0,1,0,0},
        {0,0,0,0,0,0,0,1,1,1,0,0,0},
        {0,0,0,0,0,0,0,1,1,0,0,0,0}
    };
    int expected = 6;
    auto solution = Solution1_BFS{};
    { // New scope.
        auto const start = std::chrono::steady_clock::now();
        auto const result = solution.maxAreaOfIsland(grid);
        CHECK(expected == result);
        cerr << "Elapsed time: " << elapsed_time_t{start} << '\n';
    }
    cerr << "\n";
}

TEST_CASE("Case 20")
{
    cerr << doctest::testName() << '\n';
    auto grid = vector<vector<int>>{
        {0,0,0,0,0,0,0,0},
    };
    int expected = 0;
    auto solution = Solution1_BFS{};
    { // New scope.
        auto const start = std::chrono::steady_clock::now();
        auto const result = solution.maxAreaOfIsland(grid);
        CHECK(expected == result);
        cerr << "Elapsed time: " << elapsed_time_t{start} << '\n';
    }
    cerr << "\n";
}

/*
    End of "main.cpp"
*/

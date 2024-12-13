#include <algorithm>
#include <chrono>
#include <fstream>
#include <iostream>
#include <map>
#include <queue>
#include <set>
#include <sstream>
#include <vector>

class timer
{
public:
    timer(std::string point) : m_point{point}
    {
        m_start_point = std::chrono::high_resolution_clock::now();
    }

    ~timer()
    {
        auto endclock = std::chrono::high_resolution_clock::now();
        auto start = std::chrono::time_point_cast<std::chrono::microseconds>(
                         m_start_point)
                         .time_since_epoch()
                         .count();
        auto end = std::chrono::time_point_cast<std::chrono::microseconds>(endclock)
                       .time_since_epoch()
                       .count();

        auto duration = end - start;
        double ms = duration * 0.001;

        std::cout << "time used by : " << m_point << " was : " << ms << " ms"
                  << std::endl;
    }

private:
    std::string m_point;
    std::chrono::time_point<std::chrono::high_resolution_clock> m_start_point;
};

auto findPortals(const std::vector<std::string> &maze)
{
    std::unordered_map<std::string, std::vector<std::pair<int, int>>> portals;
    int height = maze.size();
    int width = maze[0].size();

    // Iterate through the maze, excluding the outermost walls
    for (int y = 0; y < height; ++y)
    {
        for (int x = 0; x < width; ++x)
        {
            if (std::isalpha(maze[y][x]))
            {
                std::string portalName = "";
                std::pair<int, int> pos;

                if (x + 1 < width && std::isalpha(maze[y][x + 1]))
                {
                    portalName += maze[y][x];
                    portalName += maze[y][x + 1];

                    if (x > 0 && maze[y][x - 1] == '.')
                    {
                        pos = {x - 1, y};
                    }
                    else if (x + 2 < width && maze[y][x + 2] == '.')
                    {
                        pos = {x + 2, y};
                    }
                }
                else if (y + 1 < height && std::isalpha(maze[y + 1][x]))
                {
                    portalName += maze[y][x];
                    portalName += maze[y + 1][x];

                    if (y > 0 && maze[y - 1][x] == '.')
                    {
                        pos = {x, y - 1};
                    }
                    else if (y + 2 < height && maze[y + 2][x] == '.')
                    {
                        pos = {x, y + 2};
                    }
                }

                if (!portalName.empty())
                {
                    portals[portalName].push_back(pos);
                }
            }
        }
    }

    // Detect outer portals
    for (int x = 0; x < width; ++x)
    {
        if (maze[0][x] == '.' && std::isalpha(maze[1][x]) && std::isalpha(maze[2][x]))
        {
            std::string portalName = {maze[1][x], maze[2][x]};
            portals[portalName].push_back({x, 0});
        }
        if (maze[height - 1][x] == '.' && std::isalpha(maze[height - 2][x]) && std::isalpha(maze[height - 3][x]))
        {
            std::string portalName = {maze[height - 2][x], maze[height - 3][x]};
            portals[portalName].push_back({x, height - 1});
        }
    }

    for (int y = 0; y < height; ++y)
    {
        if (maze[y][0] == '.' && std::isalpha(maze[y][1]) && std::isalpha(maze[y][2]))
        {
            std::string portalName = {maze[y][1], maze[y][2]};
            portals[portalName].push_back({0, y});
        }
        if (maze[y][width - 1] == '.' && std::isalpha(maze[y][width - 2]) && std::isalpha(maze[y][width - 3]))
        {
            std::string portalName = {maze[y][width - 2], maze[y][width - 3]};
            portals[portalName].push_back({width - 1, y});
        }
    }

    return portals;
}

namespace std
{
    template <>
    struct hash<std::pair<int, int>>
    {
        size_t operator()(const std::pair<int, int> &p) const
        {
            return hash<int>{}(p.first) ^ hash<int>{}(p.second);
        }
    };
} // namespace std

// Function to build the graph for BFS
std::unordered_map<std::pair<int, int>,
                   std::vector<std::pair<std::pair<int, int>, int>>>
buildGraph(const std::vector<std::string> &maze,
           const std::unordered_map<std::string,
                                    std::vector<std::pair<int, int>>> &portals,
           bool recursive = false)
{
    std::unordered_map<std::pair<int, int>,
                       std::vector<std::pair<std::pair<int, int>, int>>>
        graph;
    int height = maze.size();
    int width = maze[0].size();

    // Helper function to check if a position is valid
    auto isValidPosition = [&](int x, int y)
    {
        return x >= 0 && x < width && y >= 0 && y < height && maze[y][x] == '.';
    };

    for (int y = 0; y < height; ++y)
    {
        for (int x = 0; x < width; ++x)
        {
            if (maze[y][x] == '.')
            {
                std::pair<int, int> pos = {x, y};
                std::vector<std::pair<std::pair<int, int>, int>> neighbors;

                // Check adjacent positions
                if (isValidPosition(x - 1, y))
                {
                    neighbors.push_back({{x - 1, y}, 0});
                }
                if (isValidPosition(x + 1, y))
                {
                    neighbors.push_back({{x + 1, y}, 0});
                }
                if (isValidPosition(x, y - 1))
                {
                    neighbors.push_back({{x, y - 1}, 0});
                }
                if (isValidPosition(x, y + 1))
                {
                    neighbors.push_back({{x, y + 1}, 0});
                }

                // Check for portals
                for (const auto &portal : portals)
                {
                    if (portal.second.size() == 2 &&
                        std::find(portal.second.begin(), portal.second.end(), pos) !=
                            portal.second.end())
                    {
                        std::pair<int, int> otherEnd =
                            portal.second[0] == pos ? portal.second[1] : portal.second[0];
                        int levelChange = 0;
                        if (recursive)
                        {
                            // Determine if the portal leads to an inner or outer level
                            if (pos.first == 2 || pos.first == width - 3 ||
                                pos.second == 2 || pos.second == height - 3)
                            {
                                levelChange = -1; // Outer portal
                            }
                            else
                            {
                                levelChange = 1; // Inner portal
                            }
                        }
                        neighbors.push_back({otherEnd, levelChange});
                    }
                }

                graph[pos] = neighbors;
            }
        }
    }

    return graph;
}

// Function to find the shortest path using BFS
int findShortestPath(
    const std::unordered_map<std::pair<int, int>,
                             std::vector<std::pair<std::pair<int, int>, int>>> &
        graph,
    const std::pair<int, int> &start,
    const std::pair<int, int> &end,
    bool recursive = false)
{
    std::queue<std::pair<std::pair<int, int>, int>> q; // Store position and level
    std::set<std::pair<std::pair<int, int>, int>> visited;

    q.push({start, 0});
    visited.insert({start, 0});

    while (!q.empty())
    {
        std::pair<int, int> currentPos = q.front().first;
        int level = q.front().second;
        int steps = q.front().second >> 16; // Extract steps from the second element
        q.pop();

        if (currentPos == end && level == 0)
        {
            return steps;
        }

        // Check if the currentPos exists in the graph
        if (graph.find(currentPos) == graph.end())
        {
            continue; // Skip if not found
        }

        for (const auto &neighbor : graph.at(currentPos))
        {
            std::pair<int, int> nextPos = neighbor.first;
            int levelChange = neighbor.second;
            int nextLevel = level + levelChange;

            if (nextLevel >= 0 &&
                visited.find({nextPos, nextLevel}) == visited.end())
            {
                int nextSteps = (steps + 1) << 16 | nextLevel; // Combine steps and level
                q.push({nextPos, nextSteps});
                visited.insert({nextPos, nextLevel});
            }
        }
    }

    return -1; // No path found
}

void task_1(std::vector<std::string> maze)
{
    auto portals = findPortals(maze);
    auto graph = buildGraph(maze, portals);

    std::pair<int, int> start, end;
    // Ensure portals "AA" and "ZZ" exist and have entries
    if (portals.count("AA") && portals["AA"].size() > 0)
    {
        start = portals["AA"][0];
    }
    else
    {
        std::cerr << "Error: Portal AA not found or has no entries." << std::endl;
        return; // Or handle the error appropriately
    }
    if (portals.count("ZZ") && portals["ZZ"].size() > 0)
    {
        end = portals["ZZ"][0];
    }
    else
    {
        std::cerr << "Error: Portal ZZ not found or has no entries." << std::endl;
        return; // Or handle the error appropriately
    }

    int pathLength = findShortestPath(graph, start, end);
    if (pathLength != -1)
    {
        std::cout << "Part 1: Shortest path length = " << pathLength << std::endl;
    }
    else
    {
        std::cout << "Part 1: No path found." << std::endl;
    }
}

void task_2(std::vector<std::string> maze) {}

int main()
{

    std::ifstream input_fd{"input/day20_input.txt"};

    std::vector<std::string> maze;
    std::string line;

    while (std::getline(input_fd, line))
        maze.push_back(line);

    {
        timer t1("task 1");
        task_1(maze);
    }

    {
        timer t1("task 2");
        task_2(maze);
    }

    return 0;
}
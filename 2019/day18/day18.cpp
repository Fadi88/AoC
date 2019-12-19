#include <iostream>
#include <fstream>
#include <vector>
#include <sstream>
#include <chrono>
#include <set>
#include <map>
#include <queue>
#include <unordered_map>


class timer {
public:
    timer(std::string point) : m_point{ point } {
        m_start_point = std::chrono::high_resolution_clock::now();
    }

    ~timer() {
        auto endclock = std::chrono::high_resolution_clock::now();
        auto start = std::chrono::time_point_cast<std::chrono::microseconds>(m_start_point).time_since_epoch().count();
        auto end = std::chrono::time_point_cast<std::chrono::microseconds>(endclock).time_since_epoch().count();

        auto duration = end - start;
        double ms = duration * 0.001;

        std::cout << "time used by : " << m_point << " was : " << ms << " ms" << std::endl;

    }

private:
    std::string m_point;
    std::chrono::time_point<std::chrono::high_resolution_clock> m_start_point;
};

struct point {
    int16_t x;
    int16_t y;
    int16_t distance;

    bool operator < (const point& other) const {
        return x < other.x && y < other.y;
    }
};

struct path {
    int16_t distance{};
    std::vector<uint8_t> doors;
};


path get_path(uint8_t p_map[81][81], point p_src, point p_dst) {
    path ret;
    ret.distance = -1;

    p_src.distance = 0;

    std::queue<point> to_visit;
    to_visit.push({ p_src });
    std::pair<int8_t, int8_t> directions[]= { std::make_pair(-1,0) , std::make_pair(1,0) , std::make_pair(0,-1), std::make_pair(0,+1) };

    while (!to_visit.empty()) {


    }


    return ret;
}

void task_1(uint8_t p_map[81][81]) {

    int8_t px{}, py{};

    std::map<uint8_t, point> keys_map;
    std::map<uint8_t, point> doors_map;

    for (uint8_t y_idx{}; y_idx < 81; ++y_idx) {
        for (uint8_t x_idx{}; x_idx < 81; ++x_idx) {

            if (p_map[y_idx][x_idx] == '@') {
                px = x_idx;
                py = y_idx;
            }

            if (p_map[y_idx][x_idx] >= 'a' && p_map[y_idx][x_idx] <= 'z') {
                keys_map[p_map[y_idx][x_idx]] = { x_idx , y_idx };
            }

            if (p_map[y_idx][x_idx] >= 'A' && p_map[y_idx][x_idx] <= 'Z') {
                doors_map[p_map[y_idx][x_idx]] = { x_idx , y_idx };
            }
        }
    }

    std::map<std::pair<uint8_t, uint8_t>, path> paths_map;

    for (auto dst_key : keys_map) {
        path tmp = get_path(p_map, { 0,0 }, dst_key.second);
        if (tmp.distance != -1)
            paths_map[{'@', dst_key.first}] = tmp;
    }

    for (auto src_key : keys_map) {
        for (auto dst_key : keys_map) {

            if (src_key.first == dst_key.first || dst_key.first > src_key.first)
                continue;

            path tmp = get_path(p_map, src_key.second, dst_key.second);

            if (tmp.distance != -1)
                paths_map[{src_key.first, dst_key.first}] = tmp;
        }

    }

}


void task_2() {

}

int main() {

    std::ifstream input_fd{ "input\\day18_input.txt" };

    std::string tmp;
    std::vector<std::string> maze_str;
    while (input_fd >> tmp) {
        maze_str.push_back(tmp);
    }

    int16_t x{}, y{};
    uint8_t maze[81][81];
    for (auto& row : maze_str) {
        for (auto& ch : row) {
            maze[y][x] = ch;
            ++x;
        }
        ++y;
        x = 0;
    }

    {
        timer t1("task 1");
        task_1(maze);
    }


    {
        timer t1("task 2");
        task_2();
    }

    return 0;
}

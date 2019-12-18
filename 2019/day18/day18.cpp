#include <iostream>
#include <fstream>
#include <vector>
#include <sstream>
#include <chrono>
#include <set>
#include <map>
#include <queue>


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


void task_1(std::map<std::pair<int8_t, int8_t>, int8_t> p_map) {

    int8_t px{}, py{};
    std::map<uint8_t, std::pair<int8_t, int8_t>> keys_map;
    std::map<uint8_t, std::pair<int8_t, int8_t>> doors_map;

    for (auto& ele : p_map) {

        if (ele.second == '@') {
            px = ele.first.first;
            py = ele.first.second;
        }

        if (ele.second >= 'a' && ele.second <= 'z') {
            keys_map[ele.second] = ele.first;
        }

        if (ele.second >= 'A' && ele.second <= 'Z') {
            doors_map[ele.second] = ele.first;
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

    std::map<std::pair<int8_t, int8_t>, int8_t> map;

    int x{}, y{};
    for (auto& row : maze_str) {
        for (auto& ch : row) {
            map[{x,y}] = ch;
            ++x;
        }
        ++y;
        x = 0;
    }

    {
        timer t1("task 1");
        task_1(map);
    }


    {
        timer t1("task 2");
        task_2();
    }

    return 0;
}

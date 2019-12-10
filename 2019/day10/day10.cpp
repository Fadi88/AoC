#include <iostream>
#include <fstream>
#include <vector>
#include <sstream>
#include <chrono>
#include <set>
#include <algorithm>

class timer {
public:
    timer(std::string point) {
        m_start_point = std::chrono::high_resolution_clock::now();
        m_point = point;
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
    uint8_t x{};
    uint8_t y{};
    uint16_t connected_points{};
};

bool float_equal(float_t lhs, float_t rhs) {
    return (std::fabs(lhs - rhs) < 0.000001);
}

void set_connected_points(std::vector<point> p_map, point& p_point) {

    for (point& tmp_pt : p_map) {

        if (tmp_pt.x == p_point.x && tmp_pt.y == p_point.y)
            continue;

        float_t  a;
        float_t  b;
        bool is_vertical{};
        bool are_connected = true;

        if (tmp_pt.x != p_point.x) {
            a = float_t(tmp_pt.y - p_point.y) / float_t(tmp_pt.x - p_point.x);
            b = tmp_pt.y - a * tmp_pt.x;

        }
        else {
            is_vertical = true;
        }

        for (point& checked_pt : p_map) {

            if ((checked_pt.x == p_point.x && checked_pt.y == p_point.y) || (checked_pt.x == tmp_pt.x && checked_pt.y == tmp_pt.y))
                continue;

            if (is_vertical) {
                if (checked_pt.x == p_point.x && checked_pt.y > std::min(tmp_pt.y, p_point.y) && checked_pt.y < std::max(tmp_pt.y, p_point.y)) {
                    are_connected = false;
                    break;
                }
            }
            else if (float_equal(checked_pt.y, a * checked_pt.x + b)) {
                if (checked_pt.y > std::min(tmp_pt.y, p_point.y) && checked_pt.y < std::max(tmp_pt.y, p_point.y) && 
                    checked_pt.x > std::min(tmp_pt.x, p_point.x) && checked_pt.x < std::max(tmp_pt.x, p_point.x)) {
                    are_connected = false;
                    break;
                }
            }

        }
        if (are_connected)
            p_point.connected_points++;
    }

}

void task_1(std::vector<point> p_map) {

    for (auto& tmp : p_map) {

        set_connected_points(p_map, tmp);
    }

}

void task_2() {

}



int main() {
    std::ifstream input_fd{ "input\\day10_input.txt" };

    std::string tmp;
    std::vector<point> map;

    uint8_t idx_y{};
    while (input_fd >> tmp) {
        uint8_t idx_x{};

        for (char tmp_chr : tmp) {

            if (tmp_chr == '#')
                map.push_back({ idx_x ,idx_y });
            ++idx_x;
        }

        ++idx_y;
    }

    {
        timer t1("task 1");
        task_1(map);
    }

    {
        timer t1("task 2");
        //task_2(cmds);
    }

    return 0;
}

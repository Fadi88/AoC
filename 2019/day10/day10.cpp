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

const double pi() { return std::atan(1) * 4; }

class point {
public:
    uint16_t x{};
    uint16_t y{};
    uint16_t connected_points{};

    double theta{};
    double R;

    bool operator == (const point& other) {
        return x == other.x && y == other.y;
    }

    bool operator < (const point& other) const {
        return theta == other.theta ? R < other.R : theta < other.theta;
    }

};


void set_connected_points(std::vector<point>& p_map) {
    std::set<float> slopes{};

    for (point& start_point : p_map) {
        slopes.clear();

        for (point& end_point : p_map) {

            if (start_point == end_point)
                continue;
            float dy = end_point.y - start_point.y;
            float dx = end_point.x - start_point.x;

            slopes.insert(std::atan2(dx, dy));

        }

        start_point.connected_points = slopes.size();
    }
}

void calc_polar_map(std::vector<point>& p_map, const point& center) {

    for (point& current_point : p_map) {
        if (current_point.operator==(center)) {
            continue;
        }

        float dy = current_point.y - center.y;
        float dx = current_point.x - center.x;

        double angle = std::atan2(dy, dx) * 180 / pi() + 90.0f;
        double dist = std::sqrt(dx * dx + dy * dy);

        current_point.theta = std::fmod(std::round(angle*100)/100 + 360.0f, 360.0f);
        current_point.R = dist;

    }
}

void task_1(std::vector<point>& p_map, point& best_point) {
    set_connected_points(p_map);

    uint16_t max{};

    for (auto& tmp : p_map) {
        if (tmp.connected_points > max) {
            max = tmp.connected_points;
            best_point = tmp;
        }

    }

}

void task_2(std::vector<point>& p_map, point& best_point) {

    uint16_t current_idx{};
    point ref_point{ 0.0f , 0.0f };

    calc_polar_map(p_map, best_point);
    
    p_map.erase(std::find(p_map.begin(), p_map.end(), best_point));

    std::sort(p_map.begin(), p_map.end());

    while (p_map.size()) {
        ++current_idx;

        auto target_point = std::lower_bound(p_map.begin(), p_map.end(), ref_point);

        if (target_point == p_map.end()) {
            ref_point.theta = 0;
            target_point = std::lower_bound(p_map.begin(), p_map.end(), ref_point);
        }
        else {
            ref_point.theta = target_point->theta + 0.00001f;
        }
        
        if (current_idx % 10 == 0) {
            std::cout << current_idx << "  x : " << target_point->x << "  y : " << target_point->y;
            std::cout << "  angle : " << target_point->theta << "  r : " << target_point->R << std::endl;
        }

        p_map.erase(target_point);
    }

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

    point center{};

    {
        timer t1("task 1");
        task_1(map, center);
    }

    {
        timer t1("task 2");
        task_2(map, center);
    }

    return 0;
}

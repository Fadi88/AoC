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

    bool operator == (const point& other) {
        return x == other.x && y == other.y;
    }

};


class polar_point {
public:
    polar_point(double p_a, double p_r) : theta{ p_a }, R{ p_r }{}

    double theta{};
    double R;

    bool operator ==(const polar_point& other) const {
        return theta == other.theta && R == other.R;
    }

    bool operator < (const polar_point& other) const {
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

std::vector<polar_point> calc_polar_map(std::vector<point>& p_map, const point& center) {
    std::vector<polar_point> ret{};

    for (point& current_point : p_map) {
        if (current_point.operator==(center)) {
            continue;
        }

        float dy = current_point.y - center.y;
        float dx = current_point.x - center.x;

        double angle = -std::atan2(dx, dy) * 180 / pi() - 90.0f;
        double dist = std::sqrt(dx * dx + dy * dy);

        ret.emplace_back(std::fmod(std::round(angle) + 360.0f, 360.0f), dist);

    }

    return ret;
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

    auto polar_map = calc_polar_map(p_map, best_point);
    uint16_t current_idx{};
    polar_point ref_point{ 0.0f , 0.0f };

    std::sort(polar_map.begin(), polar_map.end());

    while (polar_map.size()) {
        ++current_idx;

        auto target_point = std::lower_bound(polar_map.begin(), polar_map.end(), ref_point);

        if (target_point == polar_map.end()) {
            ref_point.theta = 0;
            target_point = std::lower_bound(polar_map.begin(), polar_map.end(), ref_point);
        }
        else {
            ref_point.theta = target_point->theta + 0.00001f;
        }

        auto x = std::round(best_point.x + target_point->R * std::cos((target_point->theta * pi() / 180)));
        auto y = std::round(best_point.y - target_point->R * std::sin((target_point->theta * pi() / 180)));
        

        std::cout << current_idx << " - point  was : " << target_point->theta << " , " << target_point->R;
        std::cout << " ---  x : " << std::round(x) << " y " << std::round(y) << std::endl;


        
        polar_map.erase(target_point);
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

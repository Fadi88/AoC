#include <iostream>
#include <fstream>
#include <vector>
#include <sstream>
#include <chrono>
#include <set>
#include <map>
#include <array>

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

uint32_t get_biodiversity_index(std::array<std::array<uint8_t, 5>, 5> arr) {
    uint32_t pattern{};
    uint8_t idx{};

    for (auto y : arr) {
        for (auto x : y) {
            if (x == '#')
                pattern |= 1 << idx;
            ++idx;
        }
    }

    return pattern;

}

void evlove_eris(std::array<std::array<uint8_t, 5>, 5>& arr) {
    std::array<std::array<uint8_t, 5>, 5> tmp;
    std::vector<std::pair<int8_t, int8_t>> dirs{ {0,1} , {0,-1} , {1,0} , {-1,0} };

    uint8_t infested{};
    int8_t cx{}, cy{};

    for (uint8_t y{}; y < 5; ++y) {
        for (uint8_t x{}; x < 5; ++x) {
            switch (arr[y][x]) {
            case '#':
                infested = 0;
                for (auto dir : dirs) {
                    cx = x + dir.first;
                    cy = y + dir.second;
                    if (cx < 0 || cx > 4 || cy < 0 || cy > 4)
                        continue;

                    if (arr[cy][cx] == '#')
                        ++infested;

                }
                if (infested != 1)
                    tmp[y][x] = '.';
                else
                    tmp[y][x] = '#';
                break;

            case '.':
                infested = 0;
                for (auto dir : dirs) {
                    cx = x + dir.first;
                    cy = y + dir.second;
                    if (cx < 0 || cx > 4 || cy < 0 || cy > 4)
                        continue;

                    if (arr[cy][cx] == '#')
                        ++infested;

                }
                if (infested == 1 || infested == 2)
                    tmp[y][x] = '#';
                else
                    tmp[y][x] = '.';

                break;
            default:
                throw std::runtime_error("unreconginzed pattern found on eris");

            }
        }
    }
    arr = tmp;
}

void task_1(std::array<std::array<uint8_t, 5>, 5> arr) {

    std::set<uint32_t> biodicersity_set;
    while (biodicersity_set.count(get_biodiversity_index(arr)) == 0) {
        biodicersity_set.insert(get_biodiversity_index(arr));
        evlove_eris(arr);
    }

    for (int idx{}; idx < 100; ++idx) {
        evlove_eris(arr);
        std::cout <<get_biodiversity_index(arr) << std::endl;
    }

    std::cout << "task 1 first bio diversity index repeated is : " << get_biodiversity_index(arr) << std::endl;
}


void task_2(std::array<std::array<uint8_t, 5>, 5> arr) {

    std::set<std::tuple<int16_t, int16_t, int16_t>> infested;
    std::vector<std::pair<int8_t, int8_t>> dirs{ {0,1} , {0,-1} , {1,0} , {-1,0} };


    int8_t tmp_x{}, tmp_y{};
    for (auto r : arr) {
        for (auto c : r) {
            if (c == '#')
                infested.insert({ tmp_x,tmp_y,0 });
            ++tmp_x;
        }
        ++tmp_y;
        tmp_x = 0;
    }

    for (uint8_t idx{}; idx < 200; ++idx) {
        std::set<std::tuple<int16_t, int16_t, int16_t>> new_infested{};
        for (auto& bug : infested) {
            int16_t x , y , z;
            x = std::get<0>(bug);
            y = std::get<1>(bug);
            z = std::get<2>(bug);

            for (auto& dir : dirs) {
                int16_t cx = x + dir.first;
                int16_t cy = y + dir.second;

                if (cx == 2 && cy == 2) {

                }
            }

        }

        infested = new_infested;
    }

    std::cout << "task 2 number of bugs is : " << infested.size() << std::endl;

}

int main() {

    std::ifstream input_fd{ "input\\day24_input.txt" };
    std::array<std::array<uint8_t, 5>, 5> arr{};
    std::string tmp;

    uint8_t ix{}, iy{};
    while (std::getline(input_fd, tmp)) {
        for (auto ch : tmp) {
            arr[iy][ix] = ch;
            ++ix;
        }
        ++iy;
        ix = 0;
    }

    {
        timer t1("task 1");
        task_1(arr);
    }


    {
        timer t1("task 2");
        task_2(arr);
    }

    return 0;
}

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


int8_t get_weight(uint16_t freq, uint16_t idx) {
    if (((freq + 1) % (4 * (idx + 1))) < (idx + 1)) {
        return 0;
    }
    else if (((freq + 1) % (4 * (idx + 1))) < 2 * (idx + 1)) {
        return 1;

    }
    else if (((freq + 1) % (4 * (idx + 1))) < 3 * (idx + 1)) {
        return 0;
    }
    else if (((freq + 1) % (4 * (idx + 1))) < 4 * (idx + 1)) {
        return -1;
    }
}

void task_1(std::vector <int16_t> input) {

    std::vector<int16_t> tmp;

    tmp = input;

    for (uint8_t iter{}; iter < 100; ++iter) {
        for (uint16_t out_idx{}; out_idx < input.size(); ++out_idx) {
            int32_t sum{};

            for (uint16_t in_idx{}; in_idx < input.size(); ++in_idx) {
                sum += input[in_idx] * get_weight(out_idx, in_idx);
            }
            tmp[out_idx] = std::abs(sum) / 10;
        }
        input = tmp;
    }


}

void task_2() {

}

int main() {

    std::ifstream input_fd{ "input\\day16_input.txt" };

    std::string tmp;
    input_fd >> tmp;
    tmp = "12345678";
    std::vector <int16_t> input;


    for (auto ch : tmp) {
        input.push_back(std::atoi(&ch));
    }

    {
        timer t1("task 1");
        task_1(input);
    }

    {
        timer t1("task 2");
        task_2();
    }

    return 0;
}

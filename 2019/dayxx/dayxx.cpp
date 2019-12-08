#include <iostream>
#include <fstream>
#include <vector>
#include <sstream>
#include <chrono>

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

std::vector<std::string> string2vector(std::string input_txt) {
    std::vector<std::string> ret;
    size_t pos{};
    uint16_t cmd_instance{};
    while ((pos = input_txt.find(',')) != std::string::npos) {
        ret.push_back(input_txt.substr(0, pos));
        input_txt.erase(0, pos + 1);
    }
    ret.push_back(input_txt.substr(0, pos));
    return ret;
}

void task_1() {

}

void task_2(){


}

int main() {
    std::ifstream input_fd{ "input\\day5_input.txt" };



    {
        timer t1("task 1");
        task_1();
    }
    
    {
        timer t1("task 2");
        task_2();
    }

    return 0;
}

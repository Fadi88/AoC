#include <iostream>
#include <fstream>
#include <vector>
#include <sstream>
#include <chrono>
#include <set>
#include <Windows.h>
#include <map>
#include <algorithm>
#include <queue>


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


class intcode_computer {
public:
    intcode_computer(std::vector<int64_t> p_cmd) : m_memory{ p_cmd }, m_initial_size{ p_cmd.size() }{
        std::vector<int64_t> padding(500, 0);
        std::copy(padding.begin(), padding.end(), std::back_inserter(m_memory));
    }

    void set_next_input(int32_t p_input) {
        m_next_input = p_input;
    }

    bool is_still_running()const { return !m_has_returned; }
    int64_t get_output()const { return m_output; }

    void run_cycle() {
        while (!m_has_returned) {

            auto opcode = m_memory[idx];
            uint16_t instruction = opcode % 100;


            int64_t* param1_ptr{};
            int64_t* param2_ptr{};
            int64_t* param3_ptr{};


            if (instruction != 99) {
                opcode /= 100;
                switch (opcode % 10) {
                case 0:
                    param1_ptr = &m_memory[m_memory[idx + 1]];
                    break;

                case 1:
                    param1_ptr = &m_memory[idx + 1];
                    break;

                case 2:
                    param1_ptr = &m_memory[m_relative_base + m_memory[idx + 1]];
                    break;
                }
            }

            if (m_instructions_with_3_params.find(instruction) != m_instructions_with_3_params.end()) {
                opcode /= 10;

                switch (opcode % 10) {
                case 0:
                    param2_ptr = &m_memory[m_memory[idx + 2]];
                    break;

                case 1:
                    param2_ptr = &m_memory[idx + 2];
                    break;

                case 2:
                    param2_ptr = &m_memory[m_relative_base + m_memory[idx + 2]];
                    break;
                }
            }

            if (instruction == 1 || instruction == 2 || instruction == 7 || instruction == 8) {
                opcode /= 10;

                switch (opcode % 10) {
                case 0:
                    param3_ptr = &m_memory[m_memory[idx + 3]];
                    break;

                case 2:
                    param3_ptr = &m_memory[m_relative_base + m_memory[idx + 3]];
                    break;
                }

            }

            std::size_t old_idx = idx;
            switch (instruction)
            {

            case 1:
                *param3_ptr = *param1_ptr + *param2_ptr;
                idx = old_idx != m_memory[idx + 4] ? idx + 4 : idx;
                break;

            case 2:
                *param3_ptr = *param1_ptr * *param2_ptr;
                idx = old_idx != m_memory[idx + 4] ? idx + 4 : idx;
                break;

            case 3:
                *param1_ptr = m_next_input;
                idx += 2;
                break;

            case 4:
                m_output = *param1_ptr;
                //std::cout << m_output << std::endl;
                idx += 2;
                return;

            case 5:
                idx = *param1_ptr != 0 ? *param2_ptr : idx + 3;
                break;

            case 6:
                idx = *param1_ptr == 0 ? *param2_ptr : idx + 3;
                break;

            case 7:
                *param3_ptr = *param1_ptr < *param2_ptr;
                idx = old_idx != m_memory[idx + 4] ? idx + 4 : idx;
                break;

            case 8:
                *param3_ptr = *param1_ptr == *param2_ptr;
                idx = old_idx != m_memory[idx + 4] ? idx + 4 : idx;
                break;

            case 9:
                m_relative_base += *param1_ptr;
                idx += 2;
                break;

            case 99:
                m_has_returned = true;
                idx += 1;
                break;

            default:
                throw std::runtime_error("wrong instruction in op code");
            }
        }

    }

private:
    std::vector<int64_t> m_memory;
    int32_t m_next_input{};
    int64_t m_output{};
    bool m_has_returned{};
    size_t idx{};
    size_t m_relative_base{};
    const static std::set<uint8_t> m_instructions_with_3_params;
    size_t m_initial_size{};

};

const std::set<uint8_t> intcode_computer::m_instructions_with_3_params{ 1,2,5,6,7,8 };

std::vector<int64_t> string2vector(std::string input_txt) {
    std::vector<int64_t> ret;
    size_t pos{};
    int64_t cmd_instance{};
    while ((pos = input_txt.find(',')) != std::string::npos) {
        std::stringstream{ input_txt.substr(0, pos) } >> cmd_instance;
        ret.push_back(cmd_instance);
        input_txt.erase(0, pos + 1);
    }
    std::stringstream{ input_txt.substr(0, pos) } >> cmd_instance;
    ret.push_back(cmd_instance);
    return ret;
}


uint8_t get_direction(std::pair<int16_t, int16_t> dst_pt, int16_t crt_x, int16_t crt_y) {
    if (crt_x == dst_pt.first) {
        return (dst_pt.second > crt_y) ? 1 : 2;
    }

    if (crt_y == dst_pt.second) {
        return (dst_pt.first > crt_x) ? 4 : 3;
    }

    throw std::runtime_error("not valid movement points");

}

std::map<std::pair<int16_t, int16_t>, uint8_t> get_maze(std::vector<int64_t> p_cmds) {

    std::map<std::pair<int16_t, int16_t>, uint8_t> maze{ {{0,0}, 1} };

    std::queue<std::vector<uint8_t>> to_visit{ {{}} };

    std::map <uint8_t, std::pair<int16_t, int16_t>> deltas = {
        {1 , {0,-1}}, // north
        {2 , {0,+1}}, // south
        {3 , {-1,0}}, // west
        {4 , {+1,0}}  // east
    };

    std::map<uint8_t, uint8_t> returning_direction{
        {1,2}, // north to south
        {2,1}, // south to north
        {3,4}, // west to east
        {4,3}  // east to west
    };

    while (!to_visit.empty()) {

        int16_t x{}, y{};
        intcode_computer robot{ p_cmds };

        auto current_path = to_visit.front();

        for (auto movement : current_path) { // send robot to current visted pointed 
            robot.set_next_input(movement);
            robot.run_cycle();
            x += deltas[movement].first;
            y += deltas[movement].second;
        }

        for (auto delta : deltas) { // explore adjencent teils

            robot.set_next_input(delta.first);
            robot.run_cycle();

            int16_t nx{ x + delta.second.first }, ny{ y + delta.second.second };

            if (maze.count({ nx,ny }) == 0) {
                maze[{ nx, ny }] = robot.get_output();
                if (maze[{ nx, ny }] != 0) {
                    auto new_path = current_path;
                    new_path.push_back(delta.first);
                    to_visit.push(new_path);
                    if (maze[{ nx, ny }] == 2)
                        std::cout << "path to oxygen is : " << new_path.size() << std::endl;
                }

            }

            if (robot.get_output() != 0) {
                robot.set_next_input(returning_direction[delta.first]);
                robot.run_cycle();
                if (!robot.get_output() == 1)
                    throw std::runtime_error("backtracking not working");
            }
        }

        to_visit.pop();

    }

    return maze;
}

std::map<std::pair<int16_t, int16_t>, uint8_t> task_1(std::vector<int64_t> p_cmds) {
    return get_maze(p_cmds);
}

void task_2(std::vector<int64_t> p_cmds) {
    intcode_computer app{ p_cmds };

}

int main() {

    std::ifstream input_fd{ "input\\day15_input.txt" };

    std::string tmp;
    input_fd >> tmp;

    std::map<std::pair<int16_t, int16_t>, uint8_t> maze;

    auto cmds = string2vector(tmp);
    {
        timer t1("task 1");
        maze = task_1(cmds);
    }

    {
        timer t1("task 2");
        task_2(cmds);
    }

    return 0;
}

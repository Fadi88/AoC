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


class intcode_computer {
public:
    intcode_computer(std::vector<int64_t> p_cmd) : m_memory{ p_cmd }, m_initial_size{ p_cmd.size() }{
        std::vector<int64_t> padding(3000, 0);
        std::copy(padding.begin(), padding.end(), std::back_inserter(m_memory));
    }

    void set_next_input(int32_t p_input) {
        m_next_input.push(p_input);
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
            m_output = -1;

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
            int64_t* test{ nullptr };
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
                test = param1_ptr;

                *param1_ptr = m_next_input.front();
                m_next_input.pop();
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
    std::queue<int64_t> m_next_input{};
    int64_t m_output{ -1 };
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

void task_1(std::vector<int64_t> p_cmds) {

    intcode_computer robot{ p_cmds };

    std::cout << "Task 1 :" << std::endl;

    std::string input{ "OR A T\nAND B T\nAND C T\nNOT T J\nNOT C T\nAND D J\nWALK\n" };
    for(auto ch : input)
        robot.set_next_input(ch);

    while (robot.is_still_running()) {
        robot.run_cycle();
        if (robot.get_output() < std::numeric_limits<uint8_t>::max())
            std::cout << static_cast<uint8_t>(robot.get_output());
        else
            std::cout << robot.get_output() << std::endl << std::endl;
    }
}

void task_2(std::vector<int64_t> p_cmds) {

    intcode_computer robot{ p_cmds };

    std::cout << "Task 2 :" << std::endl;

    std::string input{ "OR A T\nAND B T\nAND C T\nNOT T J\nNOT C T\nAND D J\nNOT H T\nNOT T T\nOR E T\nAND T J\nRUN\n" };
    for (auto ch : input)
        robot.set_next_input(ch);

    while (robot.is_still_running()) {
        robot.run_cycle();
        if (robot.get_output() < std::numeric_limits<uint8_t>::max())
            std::cout << static_cast<uint8_t>(robot.get_output());
        else
            std::cout << robot.get_output() << std::endl<<std::endl;
    }
}

int main() {

    std::ifstream input_fd{ "input\\day21_input.txt" };

    std::string tmp;
    input_fd >> tmp;

    auto cmds = string2vector(tmp);
    {
        timer t1("task 1");
        task_1(cmds);
    }

    {
        timer t1("task 2");
        task_2(cmds);
    }

    return 0;
}

#include <iostream>
#include <fstream>
#include <vector>
#include <sstream>
#include <chrono>
#include <set>
#include <map>

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


class amp_software {
public:
    amp_software(std::vector<int64_t> p_cmd) : m_memory{ p_cmd }, m_initial_size{ p_cmd.size() }{
        std::vector<int64_t> padding(200, 0);
        std::copy(padding.begin(), padding.end(), std::back_inserter(m_memory));

    }

    void set_next_input(int32_t p_input) {
        m_next_input = p_input;
    }

    bool is_still_running()const { return !m_has_returned; }
    int64_t get_output()const { return m_output; }
    void set_phase(uint8_t p_phase) { m_phase = p_phase; }
    void bypass_phase_set() { m_phase_set = true; }

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
                *param1_ptr
                    = !m_phase_set ? m_phase_set = true, m_phase : m_next_input;
                idx += 2;
                break;

            case 4:
                m_output = *param1_ptr;
                std::cout << m_output << std::endl;
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
    uint8_t m_phase{};
    bool m_phase_set{};
    bool m_has_returned{};
    size_t idx{};
    size_t m_relative_base{};
    const static std::set<uint8_t> m_instructions_with_3_params;
    size_t m_initial_size{};

};

const std::set<uint8_t> amp_software::m_instructions_with_3_params{ 1,2,5,6,7,8 };

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
struct panel {
    int16_t color{};
    int16_t times_painted{};
};

std::vector<std::pair<int8_t, int8_t>> movement{
    {-1,0}, //left
    {0,1}, //down
    {1,0}, //right
    {0,-1} //up
};

void task_1(std::vector<int64_t> p_cmds) {
    amp_software robot{ p_cmds };

    std::map<std::pair<int, int>, panel> haul;

    robot.bypass_phase_set();

    int16_t x{};
    int16_t y{};
    
    int8_t direction{};

    haul[{0, 0}] = { 0,0 };



    while (robot.is_still_running()) {
        robot.set_next_input(haul[{x,y}].color);
        robot.run_cycle();

        haul[{x, y}].color = robot.get_output();
        haul[{x, y}].times_painted++;

        robot.run_cycle();
        auto new_dir = robot.get_output();

        direction += new_dir == 1 ? 1 : -1;
        direction += 4;
        direction %= 4;

        x += movement[direction].first;
        y += movement[direction].second;

        if (!haul.count({ x,y })) {
            haul[{x, y}] = { 0,0 };
        }

    }
}

void task_2(std::vector<int64_t> p_cmds) {



}

int main() {
    std::ifstream input_fd{ "input\\day11_input.txt" };

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

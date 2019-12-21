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

void task_1(std::vector<int64_t> p_cmds) {

    intcode_computer robot{ p_cmds };

    uint8_t x{}, y{};
    uint8_t rx{}, ry{};

    uint32_t sum{};

    uint8_t arr[50][50];

    while (robot.is_still_running()) {
        robot.run_cycle();
        arr[y][x] = robot.get_output();

        switch (robot.get_output()) {
        case '<':
        case '>':
        case '^':
        case 'v':
            rx = x;
            ry = y;
            break;

        case 10:
            x = 0;
            ++y;
            break;

        default:
            break;
        }
        if (robot.get_output() != 10) ++x;
    }
    for (uint16_t ix{ 1 }; ix < 49; ++ix) {
        for (uint16_t iy{ 1 }; iy < 49; ++iy) {
            if (arr[iy][ix] == '#') {
                if (arr[iy - 1][ix] == '#' && arr[iy + 1][ix] == '#' && arr[iy][ix - 1] == '#' && arr[iy][ix + 1] == '#') {
                    sum += ix * iy;
                }
            }
        }
    }
    std::cout << "task 1 result is : " << sum << std::endl;
}

uint16_t count_occurence(std::string src, std::string trgt) {

    uint16_t count{};
    if (trgt.size() == 0)
        return trgt.size();
    while (src.find(trgt) != src.npos) {
        ++count;
        // erase from zero since we dont care about all the values before the target string to make search space smaller for the next iteration
        src.erase(0, src.find(trgt) + trgt.size());
    }

    return count;
}

std::string get_next_candiate(std::string path_seg, std::string current_candiate) {

    if (current_candiate.size() != 0)
        current_candiate += ",";

    path_seg.erase(0, current_candiate.size());
    if (path_seg[0] == ',')
        path_seg.erase(0, 1);

    current_candiate += path_seg.substr(0, path_seg.find(','));
    path_seg.erase(0, path_seg.find(',') + 1);
    current_candiate += ',' + path_seg.substr(0, path_seg.find(','));

    return current_candiate;
}

void task_2(std::string p_cmd_string) {
    p_cmd_string[0] = '2';
    intcode_computer robot{ string2vector(p_cmd_string) };

    // TODO : automate path generation

    std::string path{ "R,6,L,8,R,8,R,6,L,8,R,8,R,4,R,6,R,6,R,4,R,4,L,8,R,6,L,10,L,10,R,4,R,6,R,6,R,4,R,4,L,8,R,6,L,10,L,10,R,4,R,6,R,6,R,4,R,4,L,8,R,6,L,10,L,10,R,6,L,8,R,8,L,8,R,6,L,10,L,10" };


    std::vector<std::string> subroutines;
    std::string path_copy = path;

    for (int8_t idx{}; idx < 3; ++idx) {
        std::string routine_candiate{};

        while (count_occurence(path_copy, get_next_candiate(path_copy, routine_candiate)) > 2 && routine_candiate.size() < 19) {
            routine_candiate = get_next_candiate(path_copy, routine_candiate);

        }
        subroutines.push_back(routine_candiate);
        while (path_copy.find(routine_candiate) != path_copy.npos)
            path_copy.replace(path_copy.find(routine_candiate), routine_candiate.size()+1, "");

    }

    std::string seq{ path };

    for (int8_t idx{}; idx < subroutines.size(); ++idx) {
        std::string sub = subroutines[idx];
        while (seq.find(sub) != seq.npos) {
            seq.replace(seq.find(sub), sub.size(), { int8_t(idx + 'A') });
        }
    }

    for (auto ch : seq) {
        robot.set_next_input(ch);
    }
    robot.set_next_input('\n');

    for (auto& sub : subroutines) {
        for (auto ch : sub) {
            robot.set_next_input(ch);
        }
        robot.set_next_input('\n');
    }

    robot.set_next_input('n');
    robot.set_next_input('\n');

    while (robot.is_still_running()) {
        robot.run_cycle();
        std::cout << static_cast<uint8_t>(robot.get_output());

    }
    std::cout << std::endl << "task 2 dust collected is : " << robot.get_output() << std::endl;
}

int main() {

    std::ifstream input_fd{ "input\\day17_input.txt" };

    std::string tmp;
    input_fd >> tmp;

    auto cmds = string2vector(tmp);
    {
        timer t1("task 1");
        task_1(cmds);
    }


    {
        timer t1("task 2");
        task_2(tmp);
    }

    return 0;
}

#include <iostream>
#include <fstream>
#include <vector>
#include <sstream>
#include <chrono>
#include <initializer_list>
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

std::vector<int32_t> string2vector(std::string input_txt) {
    std::vector<int32_t> ret;
    size_t pos{};
    int16_t cmd_instance{};
    while ((pos = input_txt.find(',')) != std::string::npos) {
        std::stringstream{ input_txt.substr(0, pos) } >> cmd_instance;
        ret.push_back(cmd_instance);
        input_txt.erase(0, pos + 1);
    }
    std::stringstream{ input_txt.substr(0, pos) } >> cmd_instance;
    ret.push_back(cmd_instance);
    return ret;
}

int32_t get_comp_output(std::vector<int32_t> p_cmds, std::vector<uint32_t> p_inputs) {

    int32_t output_val{};

    for (std::size_t idx{}; idx < p_cmds.size();)
    {

        auto opcode = p_cmds[idx];

        auto instruction = opcode - (opcode / 100) * 100;
        int32_t param1;
        int32_t param2;

        if (instruction == 1 || instruction == 2 || instruction == 5 || instruction == 6 || instruction == 7 || instruction == 8) {
            opcode /= 100;
            if (opcode - ((opcode / 10) * 10) == 0) { //position mode 
                param1 = p_cmds[p_cmds[idx + 1]];
            }
            else {
                if (opcode - ((opcode / 10) * 10) == 1)
                    param1 = p_cmds[idx + 1];
                else
                    throw std::runtime_error("param 1 wrong mode");
            }

            opcode /= 10;
            if (opcode - ((opcode / 10) * 10) == 0) { //position mode 
                param2 = p_cmds[p_cmds[idx + 2]];
            }
            else {
                if (opcode - ((opcode / 10) * 10) == 1)
                    param2 = p_cmds[idx + 2];
                else
                    throw std::runtime_error("param 2 wrong mode");
            }
        }


        std::size_t old_idx = idx;
        switch (instruction)
        {

        case 1:
            p_cmds[p_cmds[idx + 3]] = param1 + param2;
            if (old_idx != p_cmds[idx + 4])
                idx += 4;
            break;

        case 2:
            p_cmds[p_cmds[idx + 3]] = param1 * param2;
            if (old_idx != p_cmds[idx + 4])
                idx += 4;
            break;

        case 3:
            p_cmds[p_cmds[idx + 1]] = p_inputs.front();
            p_inputs.erase(p_inputs.begin());
            idx += 2;
            break;

        case 4:
            output_val = p_cmds[p_cmds[idx + 1]];
            if (old_idx != p_cmds[idx + 2])
                idx += 2;
            break;

        case 5:
            if (param1 != 0)
                idx = param2;
            else
                idx += 3;
            break;

        case 6:
            if (param1 == 0)
                idx = param2;
            else
                idx += 3;
            break;

        case 7:
            p_cmds[p_cmds[idx + 3]] = param1 < param2;

            if (old_idx != p_cmds[idx + 4])
                idx += 4;
            break;

        case 8:
            p_cmds[p_cmds[idx + 3]] = param1 == param2;

            if (old_idx != p_cmds[idx + 4])
                idx += 4;
            break;

        case 99:
            return output_val;
        default:
            throw std::runtime_error("wrong instruction in op code");
        }
    }

    return output_val;
}

void task_1(std::vector<int32_t> p_cmds_vec) {
    uint32_t max_thrust{ 0 };

    std::vector<uint8_t> seq{ 0,1,2,3,4 };
    std::vector<uint8_t> ret{};

    do {
        uint32_t cmp0_output = get_comp_output(p_cmds_vec, { seq[0],0 });
        uint32_t cmp1_output = get_comp_output(p_cmds_vec, { seq[1],cmp0_output });
        uint32_t cmp2_output = get_comp_output(p_cmds_vec, { seq[2],cmp1_output });
        uint32_t cmp3_output = get_comp_output(p_cmds_vec, { seq[3],cmp2_output });
        uint32_t cmp4_output = get_comp_output(p_cmds_vec, { seq[4],cmp3_output });

        if (cmp4_output > max_thrust) {
            max_thrust = cmp4_output;
            ret = seq;

        }
    } while (std::next_permutation(seq.begin(), seq.end()));
    std::cout << max_thrust;
}

void task_2() {


}

int main() {
    std::ifstream input_fd{ "input\\day7_input.txt" };

    std::string tmp;
    input_fd >> tmp;

    auto cmds = string2vector(tmp);

    {
        timer t1("task 1");
        task_1(cmds);
    }

    {
        timer t1("task 2");
        task_2();
    }

    return 0;
}

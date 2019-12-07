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

class amp_software {
public:
    amp_software(std::vector<int32_t> p_cmd) : m_memory(p_cmd) {}

    void set_next_input(int32_t p_input) {
        m_next_input = p_input;
    }

    bool is_still_running()const { return !m_has_returned; }

    uint32_t get_output()const { return m_output; }
    void set_phase(uint8_t p_phase) { m_phase = p_phase; }

    void run_cycle() {
        for (; !m_has_returned && idx < m_memory.size();)
        {

            auto opcode = m_memory[idx];

            auto instruction = opcode - (opcode / 100) * 100;
            int32_t param1;
            int32_t param2;

            if (instruction == 1 || instruction == 2 || instruction == 5 || instruction == 6 || instruction == 7 || instruction == 8) {
                opcode /= 100;
                if (opcode - ((opcode / 10) * 10) == 0) { //position mode 
                    param1 = m_memory[m_memory[idx + 1]];
                }
                else {
                    if (opcode - ((opcode / 10) * 10) == 1)
                        param1 = m_memory[idx + 1];
                    else
                        throw std::runtime_error("param 1 wrong mode");
                }

                opcode /= 10;
                if (opcode - ((opcode / 10) * 10) == 0) { //position mode 
                    param2 = m_memory[m_memory[idx + 2]];
                }
                else {
                    if (opcode - ((opcode / 10) * 10) == 1)
                        param2 = m_memory[idx + 2];
                    else
                        throw std::runtime_error("param 2 wrong mode");
                }
            }


            std::size_t old_idx = idx;
            switch (instruction)
            {

            case 1:
                m_memory[m_memory[idx + 3]] = param1 + param2;
                if (old_idx != m_memory[idx + 4])
                    idx += 4;
                break;

            case 2:
                m_memory[m_memory[idx + 3]] = param1 * param2;
                if (old_idx != m_memory[idx + 4])
                    idx += 4;
                break;

            case 3:
                if (!m_phase_set) {
                    m_phase_set = true;
                    m_memory[m_memory[idx + 1]] = m_phase;
                }
                else
                    m_memory[m_memory[idx + 1]] = m_next_input;
                idx += 2;
                break;

            case 4:
                m_output = m_memory[m_memory[idx + 1]];
                idx += 2;
                return;

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
                m_memory[m_memory[idx + 3]] = param1 < param2;

                if (old_idx != m_memory[idx + 4])
                    idx += 4;
                break;

            case 8:
                m_memory[m_memory[idx + 3]] = param1 == param2;

                if (old_idx != m_memory[idx + 4])
                    idx += 4;
                break;

            case 99:
                m_has_returned = true;
                break;
            default:
                throw std::runtime_error("wrong instruction in op code");
            }
        }

    }


private:
    std::vector<int32_t> m_memory;
    int32_t m_next_input{};
    uint32_t m_output{};
    uint8_t m_phase{};
    bool m_phase_set{};
    bool m_has_returned{};
    size_t idx{};

};

void task_1(std::vector<int32_t> p_cmds_vec) {
    uint32_t max_thrust{ 0 };

    std::vector<uint8_t> seq{ 0,1,2,3,4 };
    std::vector<uint8_t> ret{};

    do {

        amp_software amp_a{ p_cmds_vec };
        amp_software amp_b{ p_cmds_vec };
        amp_software amp_c{ p_cmds_vec };
        amp_software amp_d{ p_cmds_vec };
        amp_software amp_e{ p_cmds_vec };

        amp_a.set_phase(seq[0]);
        amp_a.set_next_input(0);
        while (amp_a.is_still_running())
            amp_a.run_cycle();

        amp_b.set_phase(seq[1]);
        amp_b.set_next_input(amp_a.get_output());
        while (amp_b.is_still_running())
            amp_b.run_cycle();
        
        amp_c.set_phase(seq[2]);
        amp_c.set_next_input(amp_b.get_output());
        while (amp_c.is_still_running())
            amp_c.run_cycle();

        amp_d.set_phase(seq[3]);
        amp_d.set_next_input(amp_c.get_output());
        while (amp_d.is_still_running())
            amp_d.run_cycle();
        
        amp_e.set_phase(seq[4]);
        amp_e.set_next_input(amp_d.get_output());
        while (amp_e.is_still_running())
            amp_e.run_cycle();


        if (amp_e.get_output() > max_thrust) {
            max_thrust = amp_e.get_output();
            ret = seq;
        }
    } while (std::next_permutation(seq.begin(), seq.end()));

    std::cout << max_thrust << std::endl;
}

void task_2(std::vector<int32_t> p_cmds_vec) {

    uint32_t max_thrust{ 0 };

    std::vector<uint8_t> seq{ 5,6,7,8,9 };
    std::vector<uint8_t> ret{};

    do {

        amp_software amp_a{ p_cmds_vec }, amp_b{ p_cmds_vec }, amp_c{ p_cmds_vec }, amp_d{ p_cmds_vec }, amp_e{ p_cmds_vec };

        amp_a.set_phase(seq[0]);
        amp_b.set_phase(seq[1]);
        amp_c.set_phase(seq[2]);
        amp_d.set_phase(seq[3]);
        amp_e.set_phase(seq[4]);


        while (amp_e.is_still_running()) {

            amp_a.set_next_input(cmp4_output);
            amp_a.run_cycle();

            amp_b.set_next_input(amp_a.get_output());
            amp_b.run_cycle();

            amp_c.set_next_input(amp_b.get_output());
            amp_c.run_cycle();
            cmp2_output = amp_c.get_output();

            amp_d.set_next_input(cmp2_output);
            amp_d.run_cycle();
            cmp3_output = amp_d.get_output();

            amp_e.set_next_input(cmp3_output);
            amp_e.run_cycle();
            cmp4_output = amp_e.get_output();
        }

        if (amp_e.get_output() > max_thrust) {
            max_thrust = amp_e.get_output();
            ret = seq;

        }

    } while (std::next_permutation(seq.begin(), seq.end()));

    std::cout << max_thrust << std::endl;

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
        task_2(cmds);
    }

    return 0;
}

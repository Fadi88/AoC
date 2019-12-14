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



class reaction {
    struct compostion {
        std::string name;
        uint16_t quantity;
    };

public:
    reaction() = default;
    reaction(std::string name, uint16_t quantity) {
        output.name = name;
        output.quantity = quantity;
    }

    void add_inputs(std::string name, uint16_t quantity) {
        compostion tmp{ name, quantity };
        inputs.push_back(tmp);
    }

public:
    compostion output;
    std::vector<compostion> inputs;
};

class refinery {
public:
    std::map<std::string, reaction> reaction_map;

    void add_reaction(reaction p_reaction) {
        reaction_map[p_reaction.output.name] = p_reaction;
    }
};

void task_1(std::vector<std::string>& p_input) {

    refinery refinery_obj;

    for (auto tmp : p_input) {
        std::stringstream res = std::stringstream{ tmp.substr(tmp.find("=>") + 3) };
        std::string name;
        uint16_t weight;

        res >> weight >> name;

        reaction tmp_rec{ name, weight };

        tmp.erase(tmp.find("=>"));

        do {
            auto substr = std::stringstream{ tmp.substr(0,tmp.find(',')) };
            substr >> weight >> name;
            tmp_rec.add_inputs(name, weight);

            if (tmp.find(',') == tmp.npos) {
                tmp.clear();
            }
            else {
                tmp.erase(0, tmp.find(',') + 1);
            }

        } while (tmp.size() != 0);

        refinery_obj.add_reaction(tmp_rec);
    }


}


void task_2() {
}


int main() {
    std::vector<std::string> input;
    std::string tmp;

    std::ifstream fd{ "input\\day14_input.txt" };

    while (std::getline(fd, tmp))
        input.push_back(tmp);


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
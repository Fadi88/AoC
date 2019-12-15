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
        uint64_t quantity;
    };

public:
    reaction() = default;
    reaction(std::string name, uint64_t quantity) {
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
    std::map<std::string, uint16_t> excess;

    void add_reaction(reaction p_reaction) {
        reaction_map[p_reaction.output.name] = p_reaction;
    }

    uint64_t get_cost(std::string name, uint64_t quantity = 1) {
        uint64_t sum{};


        for (auto comp : reaction_map[name].inputs) {
            uint32_t needed_quantity = comp.quantity * quantity / reaction_map[name].output.quantity;
            if (comp.name == "ORE") {
                return quantity / reaction_map[name].output.quantity * comp.quantity;
            }
            else {
                if (excess.count(comp.name) > 0) {
                    if (excess[comp.name] > needed_quantity) {
                        excess[comp.name] -= needed_quantity;
                        needed_quantity = 0;
                    }
                    else {
                        needed_quantity -= excess[comp.name];
                        excess[comp.name] = 0;
                    }
                }
            }
            
            uint32_t generated_qunatity = reaction_map[comp.name].output.quantity * std::ceil(static_cast<float>(needed_quantity) / reaction_map[comp.name].output.quantity);

            sum += get_cost(comp.name, generated_qunatity);
            if (generated_qunatity > needed_quantity)
                excess[comp.name] += generated_qunatity - needed_quantity;
        }

        return sum;
    }
};

refinery* task_1(std::vector<std::string>& p_input) {

    refinery* refinery_obj = new refinery;

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

        refinery_obj->add_reaction(tmp_rec);
    }
    std::cout << "Task 1 ORE needed for 1 FUEL is : " << refinery_obj->get_cost("FUEL", 1) << std::endl;
    return refinery_obj;
}


void task_2(refinery* p_refinery) {
    // trial and error 
    // plotting first 10 almost shows a linear function
    // guessing starting point is 1e12 / cost of 1 fuel = 3871363
    // between 3671363 and 3771363 values changes dramatacily there is a high non lineraity


    // TODO: automate the lookup later
    std::cout << "cost of task 2 is ORE is : " << p_refinery->get_cost("FUEL", 3279311) << std::endl;
}


int main() {
    std::vector<std::string> input;
    std::string tmp;

    std::ifstream fd{ "input\\day14_input.txt" };

    while (std::getline(fd, tmp))
        input.push_back(tmp);

    refinery* refinery_obj;
    {
        timer t1("task 1");
        refinery_obj = task_1(input);

    }

    {
        timer t1("task 2");
        task_2(refinery_obj);
    }

    return 0;
}
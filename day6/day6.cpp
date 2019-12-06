#include <iostream>
#include <fstream>
#include <vector>
#include <sstream>
#include <chrono>
#include <map>
#include <algorithm>
#include <limits>

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

class system_t {

    struct node {
        node* ptr_center{nullptr};
        std::string name;
        bool is_visited{};
        uint32_t distance{};
    };

private:
    std::map<std::string, node*> m_nodes_map;

private:
    void _visit_graph(){

        for(auto& element : m_nodes_map){
            if(!element.second->is_visited){
                element.second->distance = 1 + _get_parent_distance(element.second->ptr_center);
                element.second->is_visited = true;                
            }
        }

    }

    uint32_t _get_parent_distance(node * ptr){
        if(!ptr)
            throw std::runtime_error("nullptr!");
        if(ptr->is_visited)
            return ptr->distance;
        else{
            ptr->is_visited = true;
            ptr->distance = 1 + _get_parent_distance(ptr->ptr_center);
            return ptr->distance;
        }
    
        
    }

    std::vector<std::string> _get_origin_path(std::string pt){
        std::vector<std::string> ret{};

        while(m_nodes_map[pt]->name != "COM" ){
            ret.push_back(m_nodes_map[pt]->name);
            pt = m_nodes_map[pt]->ptr_center->name;
        }

        return ret;

    }

public:
    void add_orbit(std::string p_center, std::string p_orbiter) {

        auto orbiter_node_itr = m_nodes_map.find(p_orbiter);

        node* orbiter_ptr{nullptr};

        if (orbiter_node_itr == m_nodes_map.end()) {
            orbiter_ptr = new node();
            m_nodes_map[p_orbiter] = orbiter_ptr;
            orbiter_ptr->name = p_orbiter;
        }

        orbiter_ptr = m_nodes_map[p_orbiter];

        auto center_node_itr = m_nodes_map.find(p_center);

        if (center_node_itr == m_nodes_map.end()) {
            node* center_ptr = new node();
            m_nodes_map[p_center] = center_ptr;
            center_ptr->name = p_center;

            if(p_center == "COM")
                center_ptr->is_visited = true;
        }

        orbiter_ptr->ptr_center = m_nodes_map[p_center];
    }

    uint32_t get_orbit_count(){

        uint32_t ret{};

        _visit_graph();


        for (auto& ele : m_nodes_map) {
            ret += ele.second->distance;
        }

        return ret;
    }
    
    uint32_t get_distance_between_points(std::string p_p1 ,std::string p_p2){
        auto path_p1 = _get_origin_path(p_p1);
        auto path_p2 = _get_origin_path(p_p2);

        _visit_graph();
        uint32_t ret_distance{std::numeric_limits<uint32_t>::max()};
        for(auto p1 :path_p1 ){
            for(auto p2 :path_p2 ){
                if(p1 == p2)
                {
                    auto tmp_distance =m_nodes_map[p_p1]->distance +  m_nodes_map[p_p2]->distance - 2 * m_nodes_map[p1]->distance - 2;
                    if(tmp_distance < ret_distance)
                        ret_distance = tmp_distance;
                }  
            }

        }
        return ret_distance;
    }

    ~system_t() {
        for (auto& ele : m_nodes_map) {
            delete(ele.second);
        }
    }
};



void task_1(std::map<std::string, std::string> p_orbits) {
    
    system_t system_obj;

    for (auto& ele : p_orbits) {
        system_obj.add_orbit(ele.second , ele.first);
    }
    
    std::cout << "number of orbits :"  << system_obj.get_orbit_count() <<std::endl;

}

void task_2(std::map<std::string, std::string> p_orbits , std::string p_src, std::string p_dst){

    system_t system_obj;

    for (auto& ele : p_orbits) {
        system_obj.add_orbit(ele.second , ele.first);
    }

    std::cout << "task 2 distance : " << system_obj.get_distance_between_points(p_src , p_dst)<<std::endl;
}

int main() {
    std::ifstream input_fd{ "input\\day6_input.txt" };

    std::map<std::string,std::string> orbits;

    std::string tmp;

    {
        timer t1("parsing");
        while (input_fd >> tmp) {
            std::size_t pos = tmp.find(')');
            orbits[tmp.substr(pos+1)] = tmp.substr(0,pos);
        }
    }

    {
        timer t1("task 1");
        task_1(orbits);
    }
    
    {
        timer t1("task 2");
        task_2(orbits , "YOU" , "SAN");
    }

    return 0;
}

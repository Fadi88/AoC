#include <iostream>
#include <fstream>
#include <vector>
#include <sstream>
#include <chrono>
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
class system_t {

	struct node {
		node* ptr_center{nullptr};
	};

private:
	std::map<std::string, node*> m_nodes_map;
	std::vector<std::string> m_node_list;

public:
	void add_orbit(std::string p_center, std::string p_orbiter) {

		node* orbiter_ptr = new node();
		m_nodes_map[p_orbiter] = orbiter_ptr;
		m_node_list.push_back(p_orbiter);

		auto center_node_itr = std::find(m_node_list.begin(), m_node_list.end(), p_center);

		if (center_node_itr == m_node_list.end()) {
			node* center_ptr = new node();
			m_nodes_map[p_center] = center_ptr;
			m_node_list.push_back(p_center);
		}

		orbiter_ptr->ptr_center = m_nodes_map[p_center];
	}

	uint32_t get_orbit_number() {

		uint32_t ret{};

		for (auto& ele : m_nodes_map) {
			ret++; // direct orbitting

			auto ptr_next = ele.second;
			while (ptr_next != nullptr) {
				ret++; //indirect orbitting
				ptr_next = ptr_next->ptr_center;
			}
		}

		return ret;
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


	std::cout << "number of orbits :"  << system_obj.get_orbit_number() <<std::endl;

}

void task_2(){


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
		task_2();
	}

	return 0;
}

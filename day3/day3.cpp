#include <iostream>
#include <fstream>
#include <vector>
#include <sstream>
#include <algorithm>
#include <cassert>



class circuit {

	struct point {
		int32_t x{};
		int32_t y{};
		uint32_t dist{};
	};

	struct intresction_point : point {
		uint32_t w0_dist;
		uint32_t w1_dist;
	};

	struct line {
		point start_point;
		point end_point;
	};

public:
	void fill_wire0(std::vector<std::string>& p_seq0) {
		m_wire0 = sequence2linevector(p_seq0);
	}

	void fill_wire1(std::vector<std::string>& p_seq1) {
		m_wire1 = sequence2linevector(p_seq1);
	}

	uint32_t solve_circuit_for_distance() {
		fill_intresction_points();
		return get_closest_intersection_distance();
	}

	uint32_t solve_circuit_for_depth() {
		fill_intresction_points();
		return get_closest_intersection_depth();
	}

private:
	std::vector<line> m_wire0;
	std::vector<line> m_wire1;
	std::vector<intresction_point> m_intrestion_points;

	bool get_line_intersections(line l0, line l1, intresction_point& out_param) {
		bool ret{ false };

		if (l0.start_point.x == l0.end_point.x) {
			out_param.x = l0.start_point.x;

			auto l1_xmin = std::min(l1.start_point.x, l1.end_point.x);
			auto l1_xmax = std::max(l1.start_point.x, l1.end_point.x);

			if (l1_xmin < l0.start_point.x && l1_xmax >l0.start_point.x) {
				auto l1_y= l1.end_point.y;

				auto l0_ymin = std::min(l0.start_point.y, l0.end_point.y);
				auto l0_ymax = std::max(l0.start_point.y, l0.end_point.y);

				if (l1_y > l0_ymin && l1_y < l0_ymax) {
					ret = true;
					out_param.y = l1_y;
					out_param.w0_dist = l0.start_point.dist + abs(out_param.y - l0.start_point.y);
					out_param.w1_dist = l1.start_point.dist + abs(out_param.x - l1.start_point.x);
				}

				
			}
		}
		else {
			out_param.y = l0.start_point.y;

			auto l1_ymin = std::min(l1.start_point.y, l1.end_point.y);
			auto l1_ymax = std::max(l1.start_point.y, l1.end_point.y);

			if (l1_ymin < l0.start_point.y && l1_ymax >l0.start_point.y) {
				auto l1_x = l1.end_point.x;

				auto l0_xmin = std::min(l0.start_point.x, l0.end_point.x);
				auto l0_xmax = std::max(l0.start_point.x, l0.end_point.x);
				
				if (l1_x > l0_xmin&& l1_x < l0_xmax) {
					ret = true;
					out_param.x = l1_x;
					out_param.w0_dist = l0.start_point.dist + abs(out_param.x - l0.start_point.x) ;
					out_param.w1_dist = l1.start_point.dist + abs(out_param.y - l1.start_point.y);
				}
			
			}

		}
			

		return ret;
	}
	std::vector<line> sequence2linevector(std::vector<std::string>& p_wirestrg) {

		std::vector<line> ret;

		point start_point{ 0,0,0 };
		point end_point{};
		for (auto& seq : p_wirestrg) {
			int16_t displacment = std::atoi(&seq.c_str()[1]);

			switch (seq.c_str()[0])
			{
			case 'U':
				end_point = { static_cast<int16_t>(start_point.x) , static_cast<int16_t>(start_point.y + displacment) , static_cast<uint32_t>(start_point.dist + displacment) };
				break;
			case 'D':
				end_point = { static_cast<int16_t>(start_point.x) , static_cast<int16_t>(start_point.y - displacment) , static_cast<uint32_t>(start_point.dist + displacment) };
				break;
			case 'R':
				end_point = { static_cast<int16_t>(start_point.x + displacment) , static_cast<int16_t>(start_point.y) , static_cast<uint32_t>(start_point.dist + displacment) };
				break;
			case 'L':
				end_point = { static_cast<int16_t>(start_point.x - displacment) , static_cast<int16_t>(start_point.y) , static_cast<uint32_t>(start_point.dist + displacment) };
				break;
			default:
				break;
			}

			ret.push_back(line{ start_point , end_point });

			start_point = end_point;

		}

		return ret;
	}

	void fill_intresction_points() {
		for (auto& wire0_line : m_wire0) {
			for (auto& wire1_line : m_wire1) {
				intresction_point tmp;
				auto ret = get_line_intersections(wire0_line, wire1_line, tmp);
				if (ret) 
					m_intrestion_points.emplace_back(tmp);
			}

		}
	}

	uint32_t get_closest_intersection_distance() {
		uint32_t distance{ std::numeric_limits<uint32_t>::max() };

		for (auto& pt : m_intrestion_points) {
			auto current_dist = abs(pt.x) + abs(pt.y);
			distance = std::min<uint32_t>(current_dist, distance);
		}

		return distance;

	}

	uint32_t get_closest_intersection_depth() {
		uint32_t depth{ std::numeric_limits<uint32_t>::max() };

		for (auto& pt : m_intrestion_points) {
			auto tmp_depth =
				pt.w0_dist + pt.w1_dist;
			depth = std::min(depth, tmp_depth);
		}

		return depth;
	}


};

std::vector<std::string> string2vector(std::string input_txt) {
	std::vector<std::string> ret;
	size_t pos{};
	uint16_t cmd_instance{};
	while ((pos = input_txt.find(',')) != std::string::npos) {
		ret.push_back(input_txt.substr(0, pos));
		input_txt.erase(0, pos + 1);
	}
	ret.push_back(input_txt.substr(0, pos));
	return ret;
}

void task_1(std::vector<std::string>& p_seq0, std::vector<std::string>& p_seq1) {
	circuit circuit_obj;

	circuit_obj.fill_wire0(p_seq0);
	circuit_obj.fill_wire1(p_seq1);

	std::cout<< circuit_obj.solve_circuit_for_distance() << std::endl;
}

void task_2(std::vector<std::string>& p_seq0, std::vector<std::string>& p_seq1) {
	circuit circuit_obj;

	circuit_obj.fill_wire0(p_seq0);
	circuit_obj.fill_wire1(p_seq1);

	std::cout << circuit_obj.solve_circuit_for_depth() << std::endl;


}

int main() {
	std::ifstream input_fd{ "input\\day3_input.txt" };

	std::string tmp;
	input_fd >> tmp;
	auto seq_0 = string2vector(tmp);
	tmp.clear();
	input_fd >> tmp;
	auto seq_1 = string2vector(tmp);
	
	//seq_0 = string2vector("R4,U4,R6");
	//seq_1 = string2vector("U2,R5,U3");	
	
	
	//seq_0 = string2vector("R75,D30,R83,U83,L12,D49,R71,U7,L72");
	//seq_1 = string2vector("U62,R66,U55,R34,D71,R55,D58,R83");


	//seq_0 = string2vector("R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51");
	//seq_1 = string2vector("U98,R91,D20,R16,D67,R40,U7,R15,U6,R7");

	task_1(seq_0, seq_1);
	task_2(seq_0, seq_1);

	return 0;
}

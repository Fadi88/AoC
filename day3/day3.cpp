#include <iostream>
#include <fstream>
#include <vector>
#include <sstream>



class circuit{

	struct point{
		int16_t x;
		int16_t y;
	};

	struct line{
		point start_point;
		point end_point;
	};

public:
	void fill_wire0(std::vector<std::string>& p_seq0){
		m_wire0 = sequence2linevector(p_seq0);
	}

	void fill_wire1(std::vector<std::string>& p_seq1){
		m_wire1 = sequence2linevector(p_seq1);
	}
        
        void solve_circuit(){

        }

private:

	
	std::vector<line> m_wire0;
	std::vector<line> m_wire1;
	std::vector<point> intrestion_points;

	point get_line_intersections(line l0 , line l1){

	}
	std::vector<line> sequence2linevector(std::vector<std::string>& p_wirestrg){

		std::vector<line> ret;

		point start_point{0,0};
		for(auto& seq:p_wirestrg){
			point end_point;
			int16_t displacment = std::atoi(&seq.c_str()[1]);



			switch (seq.c_str()[0])
			{
			case 'U':
				end_point = {static_cast<int16_t>(start_point.x) , static_cast<int16_t>(start_point.y + displacment)};
				break;
			case 'D':
				end_point = {static_cast<int16_t>(start_point.x) , static_cast<int16_t>(start_point.y - displacment)};
				break;
			case 'R':
				end_point = {static_cast<int16_t>(start_point.x + displacment) , static_cast<int16_t>(start_point.y)};
				break;
			case 'L':
				end_point = {static_cast<int16_t>(start_point.x - displacment) , static_cast<int16_t>(start_point.y)};
				break;
			default:
				break;
			}

			ret.push_back(line{start_point , end_point});

			start_point = end_point;

		}

		return ret;
	}

        void calc_intresction_points(){
		for(auto& wire0_line : m_wire0){
			for(auto& wire1_line : m_wire1){

			}

		}
	}


};

std::vector<std::string> string2vector(std::string input_txt) {
	std::vector<std::string> ret;
	size_t pos{};
	uint16_t cmd_instance{};
	while ((pos = input_txt.find(',')) != std::string::npos) {
		ret.push_back(input_txt.substr(0, pos) );
		input_txt.erase(0, pos + 1);
	}
	ret.push_back(input_txt.substr(0, pos));
	return ret;
}

void task_1(std::vector<std::string>& p_seq0,std::vector<std::string>& p_seq1 ){
	circuit circuit_obj;

	circuit_obj.fill_wire0(p_seq0);
	circuit_obj.fill_wire1(p_seq1);

	circuit_obj.solve_circuit();
}

int main() {
	std::ifstream input_fd{"input\\day3_input.txt"};

	    std::string tmp;
            input_fd >> tmp;
    auto seq_0 = string2vector(tmp);
	tmp.clear();
    input_fd >> tmp;
    auto seq_1 = string2vector(tmp);

    task_1(seq_0,seq_1);

	return 0;
}

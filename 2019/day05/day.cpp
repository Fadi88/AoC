#include <iostream>
#include <fstream>
#include <vector>
#include <sstream>
#include <chrono>
#include <string>
#include <cassert>

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

enum class param_mode : uint8_t {
	POSITION_MODE=0,
	IMMEDIATE_MODE=1
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

void task_1(std::vector<int32_t> p_cmds) {

	for (std::size_t idx{}; idx < p_cmds.size();)
	{

		auto opcode = p_cmds[idx];

		auto instruction = opcode - (opcode / 100) * 100;
		int32_t param1;
		int32_t param2;

		if (instruction == 1 || instruction == 2) {
			opcode /= 100;
			if (opcode - ((opcode / 10) * 10) == 0) { //position mode 
				param1= p_cmds[p_cmds[idx + 1]];
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

		switch (instruction)
		{

		case 1:
			p_cmds[p_cmds[idx + 3]] = param1 + param2;
			idx += 4;
			break;

		case 2:
			p_cmds[p_cmds[idx + 3]] = param1 * param2;
			idx += 4;
			break;

		case 3:
			p_cmds[p_cmds[idx + 1]] = 1; // hard coded for task 1 only called once as per requirement
			idx += 2;
			break;

		case 4:
			std::cout << "--!!"<< p_cmds[p_cmds[idx + 1]] << "!!-- ";
			idx += 2;
			break;

		case 99:
			return;
		default:
			throw std::runtime_error("wrong instruction in op code");
		}
	}

}

void task_2(std::vector<int32_t> p_cmds, uint16_t p_input){
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
			if(old_idx != p_cmds[idx + 4])
				idx += 4;
			break;

		case 2:
			p_cmds[p_cmds[idx + 3]] = param1 * param2;
			if (old_idx != p_cmds[idx + 4])
				idx += 4;
			break;

		case 3:
			p_cmds[p_cmds[idx + 1]] = p_input;
			idx += 2;
			break;

		case 4:
			std::cout << "--!!" << p_cmds[p_cmds[idx + 1]] << "!!-- ";
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
			return;
		default:
			throw std::runtime_error("wrong instruction in op code");
		}
	}

}

int main() {
	std::ifstream input_fd{ "input/input.txt" };

	std::string tmp;
	input_fd >> tmp;

	auto cmds = string2vector(tmp);
	
	
	{
		timer t1("task 1");
		task_1(cmds);
	}
	
	{
		
		timer t1("task 2");
		//cmds = string2vector("3,3,1105,-1,9,1101,0,0,12,4,12,99,1");
		task_2(cmds , 5);
	}

	return 0;
}

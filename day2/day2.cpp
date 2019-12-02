#include <iostream>
#include <fstream>
#include <vector>
#include <sstream>

std::vector<uint32_t> string2vector(std::string& input_txt) {
	std::vector<uint32_t> ret;
	size_t pos{};
	uint16_t cmd_instance{};
	while ((pos = input_txt.find(',')) != std::string::npos) {

		

		std::stringstream{ input_txt.substr(0, pos) } >> cmd_instance;
		ret.push_back(cmd_instance);
		input_txt.erase(0, pos + 1);
	}
	std::stringstream{ input_txt.substr(0, pos) } >> cmd_instance;
	ret.push_back(cmd_instance);
	return ret;
}

void task_1(std::vector<uint32_t>& input) {

	
	
	for (size_t idx{}; idx < input.size(); idx += 4) {

		switch (input[idx]) {
		case 1:
			input[input[idx + 3]] = input[input[idx + 1]] + input[input[idx + 2]];
			break;

		case 2:
			input[input[idx + 3]] = input[input[idx + 1]] * input[input[idx + 2]];
			break;

		case 99:
		default:
			return;

		}
	}

 }

int main() {
	std::ifstream input_fd{"input\\day2_input.txt"};

	std::string tmp;
	input_fd >> tmp;
	
	auto cmds = string2vector(tmp);
	cmds[1] = 12;
	cmds[2] = 2;
	task_1(cmds);

	std::cout << cmds[0];


	return 0;
}

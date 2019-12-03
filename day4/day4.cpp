#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>


std::vector<std::string> string2vector(std::string input_txt) {
	std::vector<std::string> ret;
	size_t pos{};
	uint16_t cmd_instance{};
	while ((pos = input_txt.find(',')) != std::string::npos) {
		std::stringstream{ input_txt.substr(0, pos) } >> cmd_instance;
		input_txt.erase(0, pos + 1);
	}
	std::stringstream{ input_txt.substr(0, pos) } >> cmd_instance;

	return ret;
}



void task_1() {

}

void task_2() {

}

int main() {
	std::ifstream input_fd{ "input\\day3_input.txt" };

	std::string tmp;
	input_fd >> tmp;
	auto seq_0 = string2vector(tmp);

	task_1();
	task_2();


	return 0;
}

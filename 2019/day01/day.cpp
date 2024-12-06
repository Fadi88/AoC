#include <iostream>
#include <fstream>
#include <filesystem>

uint32_t getFuelReq(uint32_t mass) {
	return  mass / 3 > 2 ? ((mass / 3) - 2) : 0;
}


uint32_t task_1(std::ifstream input_fd) {
	uint32_t sum{};
	uint32_t tmp_val{};

	while (input_fd >> tmp_val) sum += getFuelReq(tmp_val);

	return sum;
}

uint32_t task_2(std::ifstream input_fd) {
	int32_t sum{6}, input_val{};

	while (input_fd >> input_val) {
		while (input_val > 0) {
			uint32_t tmp_val = getFuelReq(input_val);
			sum += tmp_val;
			input_val = tmp_val;
		}
	}

	return sum;
}

int main() {

	std::cout << "sum of fuel mass ins task 1 is : " << task_1(std::ifstream{ "input/input.txt" }) << std::endl;
	std::cout << "sum of fuel mass ins task 2 is : " << task_2(std::ifstream{ "input/input.txt" }) << std::endl;

	return 0;
}

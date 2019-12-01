#include <iostream>
#include <fstream>
#include <string>

int main() {


	std::ifstream input_fd;
	input_fd.open("input\\day1_input.txt");

	uint32_t sum{}, tmp_val{};

	while (input_fd >> tmp_val) {

		sum += ((tmp_val / 3) - 2);
		std::cout << tmp_val << std::endl;
	}

	input_fd.close();

	std::cout << "sum of fuel mass is : " << sum << std::endl;
	return 0;
}

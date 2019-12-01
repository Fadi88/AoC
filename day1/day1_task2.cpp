#include <iostream>
#include <fstream>

uint32_t getFuelReq(uint32_t mass){
	return  mass / 3 > 2  ? ((mass / 3) - 2) : 0;
}

int main() {

	std::ifstream input_fd{ "input\\day1_input.txt" };
	int32_t sum{}, input_val{};

	while (input_fd >> input_val) {
		while (input_val  > 0 ) {
			uint32_t tmp_val = getFuelReq(input_val);
			sum += tmp_val;
			input_val = tmp_val;
		}
	}

	std::cout << "sum of fuel mass is : " << sum << std::endl;
	return 0;
}

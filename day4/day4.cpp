#include <iostream>
#include <string>
#include <sstream>


bool is_password_valid(const uint32_t p_input) {
	bool is_repeated{}, is_decreasing{ true };

	auto arr = std::to_string(p_input);

	for (uint8_t idx{}; idx < 5; ++idx) {
		if (arr[idx] == arr[idx + 1]) {
			is_repeated = true;
			break;
		}
	}

	for (uint8_t idx{}; idx < 5; ++idx) {
		if (arr[idx] > arr[idx + 1]) {
			is_decreasing = false;
			break;
		}
	}
	
	return is_repeated && is_decreasing;
}

void task_1(uint32_t p_lower_bound, uint32_t p_upper_bound) {

	uint16_t count{};

	for (uint32_t idx{ p_lower_bound }; idx < p_upper_bound; ++idx) {

		if (is_password_valid(idx))
			++count;
	}

	std::cout << "number of valid passwords wthing range is : " << count << std::endl;
}


void task_2() {

}

int main() {

	task_1(271973, 785961);
	task_2();


	return 0;
}

#include <iostream>
#include <string>
#include <sstream>


bool is_password_valid_1(const uint32_t p_input) {
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

bool is_password_valid_2(const uint32_t p_input) {

	bool is_decreasing{ true }, is_repeated{};

	auto arr = std::to_string(p_input);

	for (uint8_t idx{}; idx < 5; ++idx) {
		if (arr[idx] > arr[idx + 1]) {
			is_decreasing = false;
			break;
		}
	}

	for (uint8_t idx{}; idx < 5; ++idx) {
		bool is_match_found{};
		if (arr[idx] == arr[idx + 1]) {
			if (idx > 0) {
				if (idx == 4) {
					if (arr[4] != arr[3]) {
						is_repeated = true;
						break;
					}
				}
				else {
					if (arr[idx - 1] != arr[idx] && arr[idx + 1] != arr[idx + 2]) {
						is_repeated = true;
						break;
					}
				}
			}
			else {
				if (arr[idx + 1] != arr[idx + 2]) {
					is_repeated = true;
					break;
				}
			}
	
		}

	}


	return is_repeated && is_decreasing;
}

void task_1(uint32_t p_lower_bound, uint32_t p_upper_bound) {

	uint16_t count{};

	for (uint32_t idx{ p_lower_bound }; idx < p_upper_bound; ++idx) {

		if (is_password_valid_1(idx))
			++count;
	}

	std::cout << "number of valid passwords for task 1 wthing range is : " << count << std::endl;
}


void task_2(uint32_t p_lower_bound, uint32_t p_upper_bound) {
	uint16_t count{};

	for (uint32_t idx{ p_lower_bound }; idx < p_upper_bound; ++idx) {

		if (is_password_valid_2(idx))
			++count;
	}

	std::cout << "number of valid passwords for task 2 wthing range is : " << count << std::endl;

}

int main() {

	task_1(271973, 785961);
	task_2(271973, 785961);


	return 0;
}

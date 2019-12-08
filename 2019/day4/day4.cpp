#include <iostream>
#include <string>
#include <sstream>
#include <chrono>

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
bool is_password_valid_1(const uint32_t p_input) {
	bool is_repeated{}, is_decreasing{ true };

	auto arr = std::to_string(p_input);


	for (uint8_t idx{}; idx < 5; ++idx) {
		if (arr[idx] > arr[idx + 1]) {
			is_decreasing = false;
			break;
		}
	}

	if (!is_decreasing) return false;

	for (uint8_t idx{}; idx < 5; ++idx) {
		if (arr[idx] == arr[idx + 1]) {
			is_repeated = true;
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

    if(!is_decreasing) return false;

	for (auto tmp_chr : arr) {
		
		if (std::count(arr.cbegin(), arr.cend(), tmp_chr) == 2) {
			is_repeated = true;
			break;
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

	{
		timer t1{ "func 1" };
		task_1(271973, 785961);
	}

	{
		timer t1{ "func 2" };
		task_2(271973, 785961);
	}


	return 0;
}

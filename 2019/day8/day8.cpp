#include <iostream>
#include <fstream>
#include <vector>
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

std::vector<std::string> string2vector(std::string input_txt) {
	std::vector<std::string> ret;
	size_t pos{};
	uint16_t cmd_instance{};
	while ((pos = input_txt.find(',')) != std::string::npos) {
		ret.push_back(input_txt.substr(0, pos));
		input_txt.erase(0, pos + 1);
	}
	ret.push_back(input_txt.substr(0, pos));
	return ret;
}

void task_1(std::string m_input) {

    std::vector<std::vector<uint8_t>> image;

    uint16_t current_idx{};

    std::vector<uint8_t> tmp_vector;
    for (auto tmp_char : m_input) {

        tmp_vector.push_back(static_cast<uint8_t>(tmp_char));
        current_idx++;

        if (current_idx == (25 * 6)) {
            current_idx = 0;
            image.push_back(tmp_vector);
            tmp_vector.clear();
        }

    }

    uint16_t min_zeros{std::numeric_limits<uint16_t>::max()};

    std::vector<uint8_t> target_layer;
    for (auto vec : image) {
        if (std::count(vec.begin(), vec.end(), '0') < min_zeros) {
            min_zeros = std::count(vec.begin(), vec.end(), '0');
            target_layer = vec;
        }
    }
    uint16_t ones, twos;
    std::cout << "ones in target layer are : " << (ones = std::count(target_layer.begin(), target_layer.end(), '1')) <<std::endl;
    std::cout << "twos in target layer are : " << (twos = std::count(target_layer.begin(), target_layer.end(), '2')) <<std::endl;

    std::cout << " ones x twos = " << ones * twos << std::endl;

}

void task_2(std::string m_input){
    std::vector<std::vector<uint8_t>> image;

    uint16_t current_idx{};

    std::vector<uint8_t> tmp_vector;
    for (auto tmp_char : m_input) {

        tmp_vector.push_back(static_cast<uint8_t>(tmp_char));
        current_idx++;

        if (current_idx == (25 * 6)) {
            current_idx = 0;
            image.push_back(tmp_vector);
            tmp_vector.clear();
        }

    }
       
    std::vector<uint8_t> composite_img(25*6 , '2');

    for (auto layer : image) {

        for (std::size_t idx{}; idx < layer.size(); ++idx) {
            if (composite_img[idx] == '2')
                composite_img[idx] = layer[idx];
        }
    }

    for (std::size_t idx{}; idx < composite_img.size(); ++idx) {
        if (idx % 25 == 0)
            std::cout << std::endl;

        if (composite_img[idx] == '1')
            std::cout << '*';
        else
            std::cout << ' ';

    }
    std::cout << std::endl<<std::endl;
    
}

int main() {
	std::ifstream input_fd{ "input\\day8_input.txt" };

    std::string tmp;
    input_fd >> tmp;


	{
		timer t1("task 1");
		task_1(tmp);
	}
	
	{
		timer t1("task 2");
		task_2(tmp);
	}

	return 0;
}

#include <iostream>
#include <fstream>
#include <set>
#include <vector>
#include <algorithm>


uint32_t task_1(std::ifstream input_fd) {
    int32_t twos{}, threes{};
    std::string tmp_val;

    while (input_fd >> tmp_val) {

        for (const auto tmp_chr : tmp_val)
        {
            if (std::count(tmp_val.cbegin(), tmp_val.cend(), tmp_chr) == 2)
            {
                ++twos;
                break;
            }
        }
        for (const auto tmp_chr : tmp_val)
        {
            if (std::count(tmp_val.cbegin(), tmp_val.cend(), tmp_chr) == 3)
            {
                ++threes;
                break;
            }
        }
    }

    return twos * threes;
}

std::string task_2(std::ifstream input_fd) {
    std::string tmp_val;
    std::vector<std::string> ids;

    while (input_fd >> tmp_val)  ids.emplace_back(tmp_val);



    for (auto &tmp_val : ids) {
        for (const auto &cmp_val : ids) {

            if(cmp_val == tmp_val) continue; //same ID

            int mistmatch{},idx{-1};
            for(int chr_idx{} ; chr_idx < tmp_val.size() ; ++chr_idx){
                if(cmp_val[chr_idx] != tmp_val[chr_idx]){
                    ++mistmatch;
                    idx = chr_idx;
                }
                    

                if(mistmatch > 1)
                    break;

            }
            if(mistmatch == 1)
            {   
                return tmp_val.erase(  idx , 1);
            }
        }


    }
    return "";


}

int main() {

    std::cout << "task 1 is : " << task_1(std::ifstream{ "input/day02_input.txt" }) << std::endl;
    std::cout << "task 2 is : " << task_2(std::ifstream{ "input/day02_input.txt" }) << std::endl;

    return 0;
}

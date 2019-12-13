#include <iostream>
#include <chrono>
#include <array>
#include <map>
#include <unordered_map>


constexpr uint16_t ksim_steps = 1000;

constexpr std::array<std::pair<uint8_t, uint8_t>, 6> kcombination = {

    std::make_pair<uint8_t,uint8_t>(0,1),
    std::make_pair<uint8_t,uint8_t>(0,2),
    std::make_pair<uint8_t,uint8_t>(0,3),
    std::make_pair<uint8_t,uint8_t>(1,2),
    std::make_pair<uint8_t,uint8_t>(1,3),
    std::make_pair<uint8_t,uint8_t>(2,3),

};

uint64_t gcd(uint64_t a, uint64_t b) { 
    // Everything divides 0  
    if (a == 0) 
       return b; 
    if (b == 0) 
       return a; 
   
    // base case 
    if (a == b) 
        return a; 
   
    // a is greater 
    if (a > b) 
        return gcd(a-b, b); 
    return gcd(a, b-a); 
}

uint64_t lcm(uint64_t a , uint64_t b){
    return a * b /gcd(a,b);

}

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

struct vector_3d {
    int32_t x;
    int32_t y;
    int32_t z;

    bool operator ==(const vector_3d& other) const {
        return x == other.x && y == other.y && z == other.y;
    }
};

struct moon {
    vector_3d position{};
    vector_3d velocity{};

    bool operator ==(const moon& other) const {
        return position == other.position && velocity == other.velocity;
    }
};

void task_1(std::array<moon, 4> p_system) {

    for (uint16_t idx{}; idx < ksim_steps; ++idx) {
        for (auto& comb : kcombination) {
            moon& moon_1 = p_system[comb.first];
            moon& moon_2 = p_system[comb.second];

            if (moon_1.position.x < moon_2.position.x) {
                moon_1.velocity.x++;
                moon_2.velocity.x--;
            }

            if (moon_1.position.x > moon_2.position.x) {
                moon_1.velocity.x--;
                moon_2.velocity.x++;
            }

            if (moon_1.position.y < moon_2.position.y) {
                moon_1.velocity.y++;
                moon_2.velocity.y--;
            }

            if (moon_1.position.y > moon_2.position.y) {
                moon_1.velocity.y--;
                moon_2.velocity.y++;
            }

            if (moon_1.position.z < moon_2.position.z) {
                moon_1.velocity.z++;
                moon_2.velocity.z--;
            }

            if (moon_1.position.z > moon_2.position.z) {
                moon_1.velocity.z--;
                moon_2.velocity.z++;
            }

        }

        for (auto& tmp : p_system) {
            tmp.position.x += tmp.velocity.x;
            tmp.position.y += tmp.velocity.y;
            tmp.position.z += tmp.velocity.z;
        }

        if (idx % 250 == 0) {
            //std::cout << " sim step :" << idx << std::endl;
            for (auto& tmp : p_system) {
                //std::cout << "postion <" << tmp.position.x << "," << tmp.position.y << "," << tmp.position.z << "> velocity <" << tmp.velocity.x << "," << tmp.velocity.y << "," << tmp.velocity.z << ">" << std::endl;
            }
            //std::cout << std::endl;
        }

    }

    uint32_t sum{};
    for (auto& tmp : p_system) {
        auto pot = std::abs(tmp.position.x) + std::abs(tmp.position.y) + std::abs(tmp.position.z);
        auto kin = std::abs(tmp.velocity.x) + std::abs(tmp.velocity.y) + std::abs(tmp.velocity.z);

        sum += (pot * kin);
    }
    std::cout << "energy sum is " << sum << std::endl;
}
struct state {
    int32_t p0;
    int32_t v0;

    int32_t p1;
    int32_t v1;
    
    int32_t v2;
    int32_t p2;
    
    int32_t p3;
    int32_t v3;

    bool operator == (const state& other) const {
        return p0 == other.p0 && p1 == other.p1 && p2 == other.p2 && p3 == other.p3
            && v0 == other.v0 && v1 == other.v1 && v2 == other.v2 && v3 == other.v3;
    }
    
};

void print_system(const std::array<moon, 4>& p_system){
    for (auto& tmp : p_system) {
        std::cout << "postion <" << tmp.position.x << "," << tmp.position.y << "," << tmp.position.z << "> velocity <" << tmp.velocity.x << "," << tmp.velocity.y << "," << tmp.velocity.z << ">" << std::endl;
    }
    std::cout << std::endl;
}

void task_2(std::array<moon, 4> p_system) {

    uint64_t idx{ 1 };

    

    bool freq_x_found{}, freq_y_found{}, freq_z_found{};
    uint32_t x_peroid, y_peroid, z_peroid;

    state x0 = {p_system[0].position.x , p_system[0].velocity.x , p_system[1].position.x , p_system[1].velocity.x,
                p_system[2].position.x , p_system[2].velocity.x , p_system[3].position.x , p_system[3].velocity.x};
    state y0= {p_system[0].position.y , p_system[0].velocity.y , p_system[1].position.y , p_system[1].velocity.y,
                p_system[2].position.y , p_system[2].velocity.y , p_system[3].position.y , p_system[3].velocity.y};
    state z0= {p_system[0].position.z , p_system[0].velocity.z , p_system[1].position.z , p_system[1].velocity.z,
                p_system[2].position.z , p_system[2].velocity.z , p_system[3].position.z , p_system[3].velocity.z};

    while (true) {

        state x_current , y_current , z_current;

        for (auto& comb : kcombination) {
            moon& moon_1 = p_system[comb.first];
            moon& moon_2 = p_system[comb.second];

            if (moon_1.position.x < moon_2.position.x) {
                moon_1.velocity.x++;
                moon_2.velocity.x--;
            }

            if (moon_1.position.x > moon_2.position.x) {
                moon_1.velocity.x--;
                moon_2.velocity.x++;
            }

            if (moon_1.position.y < moon_2.position.y) {
                moon_1.velocity.y++;
                moon_2.velocity.y--;
            }

            if (moon_1.position.y > moon_2.position.y) {
                moon_1.velocity.y--;
                moon_2.velocity.y++;
            }

            if (moon_1.position.z < moon_2.position.z) {
                moon_1.velocity.z++;
                moon_2.velocity.z--;
            }

            if (moon_1.position.z > moon_2.position.z) {
                moon_1.velocity.z--;
                moon_2.velocity.z++;
            }

        }

        for (auto& tmp : p_system) {
            tmp.position.x += tmp.velocity.x;
            tmp.position.y += tmp.velocity.y;
            tmp.position.z += tmp.velocity.z;
        }
        x_current = {p_system[0].position.x , p_system[0].velocity.x , p_system[1].position.x , p_system[1].velocity.x,
                    p_system[2].position.x , p_system[2].velocity.x , p_system[3].position.x , p_system[3].velocity.x};
        y_current = {p_system[0].position.y , p_system[0].velocity.y , p_system[1].position.y , p_system[1].velocity.y,
                    p_system[2].position.y , p_system[2].velocity.y , p_system[3].position.y , p_system[3].velocity.y};
        z_current = {p_system[0].position.z , p_system[0].velocity.z , p_system[1].position.z , p_system[1].velocity.z,
                    p_system[2].position.z , p_system[2].velocity.z , p_system[3].position.z , p_system[3].velocity.z};
       

        if (x_current == x0 && !freq_x_found) {
            freq_x_found = true;
            x_peroid = idx;
        }

        if (y_current == y0 && !freq_y_found) {
            freq_y_found = true;
            y_peroid = idx;
        }

        if (z_current == z0 && !freq_z_found) {
            freq_z_found = true;
            z_peroid = idx;
        }

        if (freq_x_found && freq_y_found && freq_z_found) {
            break;
        }


        ++idx;
    }
    std::cout << " peroid is : " << lcm(x_peroid , lcm(y_peroid , z_peroid)) << std::endl;

}


int main() {

    std::array<moon, 4> tracked_system;

    tracked_system[0] = { {-9,-1,-1}  , {0,0,0} };
    tracked_system[1] = { {2,9,5}     , {0,0,0} };
    tracked_system[2] = { {10,18,-12} , {0,0,0} };
    tracked_system[3] = { {-6,15,-7}  , {0,0,0} };

    {
        timer t1("task 1");
        task_1(tracked_system);

    }

    {
        timer t1("task 2");
        task_2(tracked_system);

    }

    return 0;
}

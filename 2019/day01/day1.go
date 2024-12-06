package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
)

func main() {

	file, _ := os.Open("day1_input.txt")

	defer file.Close()
	scanner := bufio.NewScanner(file)

	var sum1, sum2 = 0, 0
	for scanner.Scan() {
		mod, _ := strconv.Atoi(scanner.Text())
		if mod/3 > 2 {
			sum1 += (mod / 3) - 2
		}

		for mod/3 > 2 {
			tmp := (mod / 3) - 2
			sum2 += tmp
			mod = tmp
		}

	}
	fmt.Println(sum1, sum2)

}

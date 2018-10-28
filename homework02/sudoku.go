package main

import (
	"fmt"
	"io/ioutil"
	"path/filepath"
)

func readSudoku(filename string) ([][]byte, error) {
	data, err := ioutil.ReadFile(filename)
	if err != nil {
		return nil, err
	}
	grid := group(filter(data), 9)
	return grid, nil
}

func filter(values []byte) []byte {
	filtered_values := make([]byte, 0)
	for _, v := range values {
		if (v >= '1' && v <= '9') || v == '.' {
			filtered_values = append(filtered_values, v)
		}
	}
	return filtered_values
}

func display(grid [][]byte) {
	for i := 0; i < len(grid); i++ {
		for j := 0; j < len(grid); j++ {
			fmt.Print(string(grid[i][j]))
		}
		fmt.Println()
	}
}

func group(values []byte, n int) [][]byte {
	var a[][]byte
	for i:=0; i<len(values); i+=n {
		a=append(a,values[i:i+n])
	}
	return a
}

func getRow(grid [][]byte, row int) []byte {
	return grid[row]
}

func getCol(grid [][]byte, col int) []byte {
	var column[]byte
	for i:=0; i<len(grid); i++ {
		column=append(column,grid[i][col])
	}
	return column
}

func getBlock(grid [][]byte, row int, col int) []byte {
	var a[]byte
	subrow := row // 3 * 3
    subcol := col // 3 * 3
    for i:=0; i<3; i++ {
    	for j:=0; j<3; j++ {
    		a=append(a,grid[subrow+i][subcol+j])
    	}
    }
    return a
}

func findEmptyPosition(grid [][]byte) (int, int) {
	for row:=0;row<len(grid);row++{
		for col:=0;col<len(grid);col++{
			if grid[row][col] == '.' {
				return row, col
			}
		}

	}
	return -1,-1
}

func contains(values []byte, search byte) bool {
	for _, v := range values {
		if v == search {
			return true
		}
	}
	return false
}

func findPossibleValues(grid [][]byte, row int, col int) []byte {
	var Values []byte
	a:=[]byte("123456789")
	row1:=getRow(grid, row)
	col1:=getCol(grid, col)
	block1:=getBlock(grid,row,col)
	for i:=0;i<9;i++{
		flag:=false
		for j:=0;j<9;j++{
			if (a[i]==row1[j])||(a[i]==col1[j])||(a[i]==block1[j]) {
				flag=true
			}
		}
		if flag==false {
			Values = append(Values,a[i])
			}
	}
	return Values
}

func solve(grid [][]byte) ([][]byte, bool) {
	row,col:=findEmptyPosition(grid)
	if (row == -1){
		return grid, true
	}
	for _,value:=range(findPossibleValues(grid,row,col)){
		grid[row][col] = value
		solution, answ:= solve(grid)
		if answ{
			return solution,answ
		}
	}
	grid[row][col]= '.'
	var none[][]byte
	return none,false
}

func checkSolution(grid [][]byte) bool {
	// PUT YOUR CODE HERE
	return 0
}

func generateSudoku(N int) [][]byte {
	// PUT YOUR CODE HERE
	return 0
}

func main() {
	puzzles, err := filepath.Glob("puzzle*.txt")
	if err != nil {
		fmt.Printf("Could not find any puzzles")
		return
	}
	for _, fname := range puzzles {
		go func(fname string) {
			grid, _ := readSudoku(fname)
			solution, _ := solve(grid)
			fmt.Println("Solution for", fname)
			display(solution)
		}(fname)
	}
	var input string
	fmt.Scanln(&input)
}
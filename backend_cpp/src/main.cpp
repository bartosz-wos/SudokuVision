#include "../include/DLX.h"

#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <sstream>
#include <cmath>
#include <chrono>

int N = 0;
int K = 0;

int cell_constraint(int r, int c){
	return r * N + c;
}

int row_constraint(int r, int c){
	return N * N + r * N + c;
}

int col_constraint(int r, int c){
	return 2 * N * N + r * N + c;
}

int box_constraint(int r, int c, int d){
	int box = (r / K) * K + (c / K);
	return 3 * N * N + box * N + d;
}

void decode_row_id(int row_id, int& r, int& c, int& d){
	d = row_id % N;
	c = (row_id / N) % N;
	r = row_id / (N * N);
}

void build_sudoku_matrix(DLX& engine, const std::vector<std::vector<int>>& board){
	for(int r = 0; r < N; r++){
		for(int c = 0; c < N; c++){
			int val = board[r][c];

			for(int d = 0; d < N; d++){
				if(val != 0 && val != d + 1)
					continue;

				int row_id = r * N * N + c * N + d;

				std::vector<int> row_constraints = {
					cell_constraint(r,c),
					row_constraint(r, d),
					col_constraint(c, d),
					box_constraint(r, c, d)
				};

				engine.add_row(row_id, row_constraints);
			}
		}
	}
}

int main(){
	std::ifstream file("data/board.txt");
	if(!file.is_open()){
		std::cerr << "\033[1;31m[!] Error: Couldn't find file data/board.txt\033[0m" << std::endl;
		return 1;
	}

	std::vector<std::vector<int>> board;
	std::string line;

	while(getline(file, line)){
		std::stringstream ss(line);
		int val;
		std::vector<int> row;

		while(ss >> val){
			row.push_back(val);
		}
		if(!row.empty()){
			board.push_back(row);
		}
	}

	file.close();

	if(board.empty()){
		std::cerr << "\033[1;31m[!] Error: The file is empty!\033[0m" << std::endl;
		return 1;
	}

	N = board.size();
	K = round(sqrt(N));

	if(K * K != N || board[0].size() != (size_t)N){
		std::cerr << "\033[1;31m[!] Error: Wrong board dimensions. Detected " << N << "x" << board[0].size() << ", but should be NxN, where N is a perfect squre.\033[0m" << std::endl;
		return 1;
	}

	int universe_size = 4 * N * N;
	DLX engine(universe_size);

	auto start_time = std::chrono::high_resolution_clock::now();

	build_sudoku_matrix(engine, board);

	std::vector<int> solution;
	bool solved = engine.solve(solution);

	auto end_time = std::chrono::high_resolution_clock::now();
	auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end_time-start_time).count();

	std::cout << "\n\033[1;32m[V] Sudoku Vision DLX [Universal " << N << "x" << N << " Engine]\033[0m]" << std::endl;
	std::cout << "____________________________________________" << std::endl;

	if(solved){
		std::vector<std::vector<int>> solved_board(N, std::vector<int>(N, 0));
		for(int row_id : solution){
			int r, c, d;
			decode_row_id(row_id, r, c, d);
			solved_board[r][c] = d + 1;
		}

		std::cout << "[+] Found the solution (Time: \033[1;36m" << duration << " microseconds\033[0m!)\n" << std::endl;

		std::ofstream out_file("data/solved_board.txt");
		if(!out_file.is_open()){
			std::cerr << "\033[1;31m[!] Error: Couldn't write to data/solved_board.txt\033[0m" << std::endl;
			return 1;
		}

		for(int i = 0; i < N; i++){
			for(int j = 0; j < N; j++){
				std::cout << solved_board[i][j] << ' ';
				out_file << solved_board[i][j] << " \n"[j == N - 1];
			}
			std::cout << std::endl;
		}

		out_file.close();
	}else{
		std::cout << "\033[1;31m[-] Error: Sudoku has no solution!\033[0m" << std::endl;
		return 2;
	}

	return 0;
}

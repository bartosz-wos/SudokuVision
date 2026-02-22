#include "../include/DLX.h"
#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <chrono>

using namespace std;

int get_cell_constraint(int r, int c) {
    return r * 9 + c;
}
int get_row_constraint(int r, int d) {
    return 81 + r * 9 + d;
}
int get_col_constraint(int c, int d) {
    return 162 + c * 9 + d;
}
int get_box_constraint(int r, int c, int d) {
    int box = (r / 3) * 3 + (c / 3);
    return 243 + box * 9 + d;
}

void decode_row_id(int row_id, int &r, int &c, int &d) {
    d = row_id % 9;
    c = (row_id / 9) % 9;
    r = row_id / 81;
}

void build_sudoku_matrix(DLX& engine, const vector<string>& board) {
    for (int r = 0; r < 9; ++r) {
        for (int c = 0; c < 9; ++c) {
            int current_val = board[r][c] - '0';
            
            for (int d = 0; d < 9; ++d) {
                if (current_val != 0 && current_val != d + 1) continue;

                int row_id = r * 81 + c * 9 + d;
                vector<int> row_constraints = {
                    get_cell_constraint(r, c),
                    get_row_constraint(r, d),
                    get_col_constraint(c, d),
                    get_box_constraint(r, c, d)
                };
                
                engine.add_row(row_id, row_constraints);
            }
        }
    }
}

int main() {
    ifstream file("../data/p096_sudoku.txt");
    if (!file.is_open()) {
        return 1;
    }

    string line;
    int solved_count = 0;
    int sum = 0;
    
    auto start_time = chrono::high_resolution_clock::now();

    while (getline(file, line)) {
        if (line.substr(0, 4) == "Grid") {
            vector<string> board(9);
            for (int i = 0; i < 9; ++i) {
                getline(file, board[i]);
            }

            DLX engine(324);
            build_sudoku_matrix(engine, board);

            vector<int> solution;
            if (engine.solve(solution)) {
                solved_count++;
                
                int r, c, d;
                int top_left[3] = {0, 0, 0};
                for(int row_id : solution){
                    decode_row_id(row_id, r, c, d);
                    if(r == 0 && c < 3){
                        top_left[c] = d + 1;
                    }
                }
                sum += (top_left[0] * 100 + top_left[1] * 10 + top_left[2]);

            } else {
                cerr << "Failed to solve grid." << endl;
            }
        }
    }

    auto end_time = chrono::high_resolution_clock::now();
    auto duration = chrono::duration_cast<chrono::milliseconds>(end_time - start_time).count();

    cout << "\033[1;32m[V] Sudoku Vision DLX Core\033[0m" << endl;
    cout << "--------------------------------" << endl;
    cout << "Grids Solved: " << solved_count << "/50" << endl;
    cout << "Project Euler 96 Sum: \033[1;33m" << sum << "\033[0m" << endl;
    cout << "Total Time: \033[1;36m" << duration << " ms\033[0m" << endl;

    return 0;
}

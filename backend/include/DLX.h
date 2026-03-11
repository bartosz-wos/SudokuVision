#ifndef DLX_H
#define DLX_H

#include <iostream>
#include <vector>

struct Node{
	Node *left;
	Node *right;
	Node *up;
	Node *down;
	Node *column;

	int row_id;
	int col_id;
	int size;
};

class DLX{
private:
	Node *head;
	std::vector<Node*> columns;
	std::vector<Node*> current_solution;
	std::vector<int> best_solution;
	bool solution_found;

	// Dancing Links
	void cover(Node *c);
	void uncover(Node *c);

	void search(int k);

public:
	DLX(int column_num);
	~DLX();
	
	void add_row(int row_id, const std::vector<int>& column_idx);

	bool solve(std::vector<int>& output_solution);
};

#endif

#include "../include/DLX.h"

DLX::DLX(int column_num){
	head = new Node();
	head->right = head;
	head->left = head;
	head->up = head;
	head->down = head;
	head->column = head;
	head->row_id = -1;
	head->col_id = -1;
	head->size = 0;

	columns.resize(column_num);
	Node* current = head;

	for(int i = 0; i < column_num; i++){
		Node *new_col = new Node();
		new_col->size = 0;
		new_col->up = new_col;
		new_col->down = new_col;
		new_col->column = new_col;
		new_col->row_id = -1;
		new_col->col_id = i;

		new_col->left = current;
		new_col->right = head;
		current->right = new_col;
		head->left = new_col;

		current = new_col;
		columns[i] = new_col;
	}

	solution_found = false;
}

void DLX::cover(Node *c){
	c->right->left = c->left;
	c->left->right = c->right;

	for(Node *i = c->down; i != c; i = i->down){
		for(Node *j = i->right; j != i; j = j->right){
			j->down->up = j->up;
			j->up->down = j->down;
			j->column->size--;
		}
	}
}

void DLX::uncover(Node *c){
	for(Node *i = c->up; i != c; i = i->up){
		for(Node *j = i->left; j != i; j = j->left){
			j->column->size++;
			j->down->up = j;
			j->up->down = j;
		}
	}
	
	c->right->left = c;
	c->left->right = c;
}

void DLX::add_row(int row_id, const std::vector<int>& column_idx){
	if(column_idx.empty())
		return;

	Node *first = nullptr;
	for(int col : column_idx){
		Node *column_head = columns[col];
		Node *new_node = new Node();
		new_node->row_id = row_id;
		new_node->col_id = col;
		new_node->column = column_head;

		new_node->up = column_head->up;
		new_node->down = column_head;
		column_head->up->down = new_node;
		column_head->up = new_node;
		column_head->size++;

		if(first == nullptr){
			first = new_node;
			first->left = first;
			first->right = first;
		}else{
			new_node->left = first->left;
			new_node->right = first;
			first->left->right = new_node;
			first->left = new_node;
		}
	}
}

void DLX::search(int k){
	if(solution_found)
		return;

	if(head->right == head){
		solution_found = true;
		for(Node *n : current_solution){
			best_solution.push_back(n->row_id);
		}
		return;
	}

	Node *c = head->right;
	for(Node *i = c->right; i != head; i = i->right){
		if(i->size < c->size){
			c = i;
		}
	}

	cover(c);

	for(Node *r = c->down; r != c; r = r->down){
		current_solution.push_back(r);

		for(Node *j = r->right; j != r; j = j->right){
			cover(j->column);
		}

		search(k + 1);

		r = current_solution.back();
		current_solution.pop_back();

		for(Node *j = r->left; j != r; j = j->left){
			uncover(j->column);
		}
	}

	uncover(c);
}

bool DLX::solve(std::vector<int>& output_solution){
	solution_found = false;
	current_solution.clear();
	best_solution.clear();

	search(0);

	if(solution_found){
		output_solution = best_solution;
	}

	return solution_found;
}

DLX::~DLX(){
	for(Node *col : columns){
		Node *current = col->down;
		while(current != col){
			Node *next = current->down;
			delete current;
			current = next;
		}
		delete col;
	}
	delete head;
}

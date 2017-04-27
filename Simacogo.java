//Jasmine Farley

import java.util.LinkedList;
import java.util.Arrays;
import java.util.Scanner;

public class Simacogo {
	
	private static class Node{

		//The node class stores info about the current state of the board
		//having the variables boardstate which is a character 2d array that 
		//keeps track of the position of the moves, max score which is the ai score, 
		//min score which is the player move, best move which is an interger that 
		//represents the column of the best move that would give the AI can make, 
		//and a Linked list of all of the board state successors.
		
		private char[][] boardstate = new char[9][9];
		private int bestmove; 
		private int ai_score;
		private int player_score;
		private LinkedList<Node> children; 

		
		private Node(){
			this.bestmove = 0;
			this.player_score = 0;
			this.ai_score = 0;
			this.boardstate = newBoard();
			this.children = new LinkedList<Node>();

		}
		
		private Node(char[][] boardstate, int ai_score, int player_score){
			this.boardstate = boardstate;
			this.ai_score = ai_score;
			this.player_score = player_score;
		}
		
		private Node (char [][] boardstate){
			this.boardstate = boardstate;
		}
		
		private Node(int bestscore){
			this.bestmove = bestmove;
		}
		
		private char[][] newBoard(){
			for (int i=0; i<9; i++){
				for(int j=0; j<9; j++){
					this.boardstate[i][j] = '_';
				}
			}
			return this.boardstate;
		}
		
		
		private void printBoard(){
			for(int i=0; i<9; i++){
				for(int j=0; j<9; j++){
					System.out.print(this.boardstate[i][j] + " ");
				}
				System.out.println();
			}
			System.out.println("1 2 3 4 5 6 7 8 9");
		}
		
		private void getScore(){
			this.ai_score = this.calc_aiscore();
			this.player_score = this.calc_playerscore();
			
			System.out.println("Computer: " + ai_score );
			System.out.println("Player: " + player_score );
		}
		
		private int calc_aiscore(){
			int score = 0;
			
			for(int i=0;i<9;i++){
				for(int j=0;j<9;j++){
					if ( this.boardstate[i][j] =='X'){

						if (i<8) {
							if ( this.boardstate[i+1][j] =='X'){
								score = score + 2;
							}
						}

						if (j<8) {
							
							if ( this.boardstate[i][j+1]== 'X'){
								score = score + 2;
							}
						}
						
						if ( j<8 && i>0){
							
							if ( this.boardstate[i-1][j+1]=='X'){
								score = score + 1;
							}
						}
						if (i<8 && j<8){
							if ( this.boardstate[i+1][j+1] =='X' ){
								score = score + 1;
							}
						}
					}
				}
			}
			return score;
		}
		
		private int calc_playerscore(){
			int score=0;
			
			for(int i=0;i<9;i++){
				for(int j=0;j<9;j++){
					if(this.boardstate[i][j] =='O'){
						if(i<8){
							if(this.boardstate[i+1][j] =='O'){
								score = score +2 ;
							}
						}
						if(j<8){
							if(this.boardstate[i][j+1]=='O'){
								score = score + 2;
							}
						}
						if(j<8&&i>0){
							if(this.boardstate[i-1][j+1]=='O'){
								score= score +1;
							}
						}
						if(i<8&&j<8){
							if(this.boardstate[i+1][j+1]=='O'){
								score = score + 1;
							}
						}
						
					}
				}
				
			}
			return score;
		}
		
		private LinkedList<Node> AI_getSuccessors(){
			
			this.children = new LinkedList<Node> ();
			
			for (int i=0; i<9; i++){
				for (int j=8; j<9; j++){
					if (this.boardstate[i][j] == '_'){
						children.add(AI_newstate(this, i, j));
						break;
					}
				}
			}
			
			return this.children; 
		}

		private LinkedList<Node> player_getSuccessors(){
			this.children=new LinkedList<Node>();
				for(int j=0;j<9;j++){
					for(int i=8; i>-1; i--){
						if(this.boardstate[i][j]=='_'){
							children.add(Player_newstate(this,i,j));
							break;
						}
					}
				}
			return this.children;
		}
		
		public String toString(){
			String board = Arrays.deepToString(boardstate);
			String children =this.children.toString();
			return "current board: " + board + "\n" +" children" + children;
		}
	}

	private static Node AI_newstate(Node node, int i, int j) {
		// Node clone = new Node (node.boardstate);
		// clone.boardstate[i][j]='X'; 
		// System.out.println("AI Clone\n" + Arrays.deepToString(clone.boardstate));
		char [][] board_copy = new char[node.boardstate.length][];
		for (int l = 0; l< node.boardstate.length; i++){
			board_copy[l] = node.boardstate[l].clone();
		}
		board_copy[i][j] = 'X';
		Node new_node = new Node (board_copy);
		return new Node(board_copy,new_node.calc_aiscore(),new_node.calc_playerscore());
	}

	private static Node Player_newstate(Node node, int i, int j) {
		// Node clone= new Node (node.boardstate);
		// clone.boardstate[i][j]='O'; 
		// System.out.println("Player Clone \n" + Arrays.deepToString(clone.boardstate));
		// return new Node(clone.boardstate,clone.calc_aiscore(),clone.calc_playerscore());
		char [][] board_copy = new char[node.boardstate.length][];
		for (int l = 0; l< node.boardstate.length; i++){
			board_copy[l] = node.boardstate[l].clone();
		}
		board_copy[i][j] = 'O';
		Node new_node = new Node (board_copy);
		return new Node(board_copy,new_node.calc_aiscore(),new_node.calc_playerscore());
	}

	private static Node player_move (int col, Node current_node){
		Node new_node = new Node();
		for (int i = 8; i>-1; i--){
			if(current_node.boardstate[i][col] =='_'){
				current_node.boardstate[i][col] ='O';
				break;
			}
		}
		new_node = current_node;
		return new_node;
	}

	private static Node ai_move (int col, Node current_node){
		Node new_node = new Node();
		for (int i = 8; i>-1; i--){
			if(current_node.boardstate[i][col] =='_'){
				current_node.boardstate[i][col] ='X';
				break;
			}
		}
		new_node = current_node;
		return new_node;
	}
	
	private static Boolean column_check (int col, Node current_node){
		if ( current_node.boardstate[0][col] == '_'){
			return false;
		}
		return true;
	}
	
	private static Boolean board_check ( Node current_node){
		for (int i = 0; i<9; i++){
			if ( current_node.boardstate[0][i] == '_'){
				return false;
			}
		}
		return true;
	}
	
	public static Node minimax(Node node,int depth,Boolean ai){   
		//this method returns a Node with the best posssible move. 
		//Taking the current state of the board, the depth (which is plys), 
		//and Boolean if it is the AI playing or not. IT then goes through the 
		//algorithm to find the max(move that would give the highest score) 
		//for the ai from the possible moves that the player can make.
		
		if(depth==0||board_check(node)){
			node.bestmove=node.calc_playerscore()-node.calc_aiscore();
			return node; 
		}
		if(ai){
			Node bestscore=new Node(Integer.MIN_VALUE);
			//LinkedList<Node> children=node.AI_getSuccessors;
			node.children= node.AI_getSuccessors();
			while(node.children.size()>0){ 
				Node child=node.children.pop();
				Node score=minimax(child,depth-1,false);
				if(score.bestmove>bestscore.bestmove){
					node.bestmove=node.bestmove+score.bestmove;
				}
			}	
			return node;
		}
		else{
			Node bestscore=new Node(Integer.MAX_VALUE);
			// LinkedList<Node> children=getMovesmin(node);
			node.children=node.player_getSuccessors();
			while(node.children.size()>0){
				Node child=node.children.pop();
				Node score=minimax(child,depth-1,true);
				if(score.bestmove<bestscore.bestmove){
					node.bestmove=node.bestmove+score.bestmove;
				}
			}
			return node;
		}
	}
	
	
	
	private static void play_simacogo(int plys)
	{
		//This is where more logic happens, a node is initialized with a blank board and an 
		//interger to represent the column is initialized. Then there is a while loop that keeps
		//asking the player to choose a column until the board is full, there are a few variables 
		//and methods that prevents the player from making illegal moves including a Boolean varaible 
		//"possiblemove" and "column_check" that checks if a column is full before applying a move. 
		//After a possible move is done, the while loop breaks and a new Node is initalized 
		//for the AI which calls the minimax method to find the max move of the 
		//current state of the board. It chooses the child with the highest possible move then plays it. 
		//During this time the score is also printed.
		
		Node current_board=new Node();
		int column = 0;
		Scanner game_scanner = new Scanner(System.in);
		while(!board_check(current_board)){
			Boolean possiblemove=true;
			current_board.printBoard() ;
			while( possiblemove){
				System.out.print("Please Choose a column 1 through 9: ");
				column = Integer.parseInt(game_scanner.next())-1;
				if(-1 < column && column < 9 && !column_check(column,current_board)){
					possiblemove = false;
				}
			}
			
			current_board = player_move(column,current_board);
			current_board.printBoard();
			if (board_check(current_board))break;
			Node ai = minimax(current_board,plys,true);
			System.out.println (ai);
			Node aimove=ai.children.pop();
			while (ai.children.size()>0){
				Node move=ai.children.pop();
			 	if (move.bestmove>aimove.bestmove){
					 aimove=move;
			 	}
			 }
			current_board = aimove;
			current_board.getScore();
			}
			
			current_board.getScore();
			game_scanner.close();
	}
	
	public static void main(String[] args) {
		// Just lays out the logic, asking how many plys should the AI perform for the algorithm, then it passes it into the simacogo method
		Scanner scanner = new Scanner(System.in);
		System.out.println("How many plys?(1-9) :");
		int plys = scanner.nextInt();
		play_simacogo(plys);
		scanner.close();
	}
}

/**
To implement the judge, you need to implement a class called GameState
It represents a possible state of the game. A template is provided for you.

Judge for two player perfect Info games

 * 
 * 1. Judge sends Player 1 a initialising message
 * 2. Judge sends Player 2 a initialising message
 * 
 * while (1):
 * 	Player 1 sends a move to judge
 *  Judge sends that move to player 2
 * 	Player 2 sends a move to judge
 *  Judge sends that move to player 1

Notes:
	All messages passed and received should have no newline
    
**/

#include <bits/stdc++.h>
#include <cstdlib>
#include <iostream>
#include <string>
#include <sstream>
using namespace std;


const std::string playerSymbols = "OX";
const char emptySymbol = '.';

class gameState
{
private:
    std::string board[3];
    int currentPlayer;
    
    char commonSymbol(char a, char b, char c) {
        if (a == b && b == c)   return a;
        return emptySymbol;
    }

    bool isFull() {
        for (int i=0; i<3; i++) 
            for (int j=0; j<3; j++)
                if (board[i][j] == '.')
                    return false;
        return true;
    }

    bool hasWon(char symbol) {
        for (int i=0; i<3; i++) {
            if (board[i][0] == symbol && board[i][1] == symbol && board[i][2] == symbol) return true;
            if (board[0][i] == symbol && board[1][i] == symbol && board[2][i] == symbol) return true;
        }
        if (board[0][0] == symbol && board[1][1] == symbol && board[2][2] == symbol) return true;
        if (board[0][2] == symbol && board[1][1] == symbol && board[2][0] == symbol) return true;
        return false;
    }
public:
    static gameState initialState() {
        /** 
         * Construct and return initial state
        */

        gameState state;
        std::string R(3, emptySymbol);
        state.board[0] = R;
        state.board[1] = R;
        state.board[2] = R;
        state.currentPlayer = 0;
        return state;
    }
    
    static std::string initMessage(int player){
        /** initial message to either player
         * Should include any initial parameters
         * such as moveorder, initial state, etc.
         * Should have no newlines
         */
        return std::to_string(player);
    }
    
    int playerToMove() {
        /** 
         * Should return
         * 0 if first player should move 
         * 1 if second player should move
        */
        return currentPlayer;
    }
    
    bool apply(std::string moveString) {
        /** 
         * Should return
         * 0 if invalid move or incorrect format
         * 1 if correct move and update state
        */
        std::stringstream ss;
        ss<<moveString;
       
        int x, y;
        if (!(ss>>x>>y))        return false;
        if (x < 0 || x >= 3)     return false;
        if (y < 0 || y >= 3)     return false;
        if (board[x][y] != emptySymbol)  return false;

        board[x][y] = playerSymbols[currentPlayer];
        currentPlayer ^= 1;
        return true;
    }

    int result(string &reason) {
        /** 
         * Should return
         * -1 if no result yet
         * 0 if first player wins, 
         * 1 if second player wins,
         * 2 if draw
         * If the match has a result, 
         * reason should include the reason, 
         * this will be saved in JSON file
        */

        if (hasWon(playerSymbols[0]))   {
            reason = "Player 1 made three in a row";
            return 0;
        }
        else if (hasWon(playerSymbols[1]))   {
            reason = "Player 2 made three in a row";
            return 0;
        }
        else if (isFull())   {
            reason = "No moves left for either player";
            return 0;
        }
        else return -1;    
    }

    std::string toString() {
        /** Visual representation of board.
         * Must if you want to save initial state to Match History
         * Otherwise only used for logging purposes and may be left empty
        */
       std::string ans;
       ans += "Player " + std::to_string(currentPlayer) + " to move\n";
       ans += board[0] + "\n";
       ans += board[1] + "\n";
       ans += board[2] + "\n";
       return ans;
    }
};

struct MatchHistory{
    string result, reason;
    vector<string> moves;
    gameState initialState;

    static string format(string s) {
        string ans = "\"";
        for (char c: s) {
            if (c == '\n')  ans += "\\n";
            else            ans += c;
        }
        ans += "\"";
        return ans;
    }

    string JSON() {
        string ans;
        ans += "{\n";
        ans += "\t" + format("Result") + ":" + format(result) + ",\n";
        ans += "\t" + format("Reason") + ":" + format(reason) + ",\n";
        ans += "\t" + format("Initial State") + ":" + format(initialState.toString()) + ",\n";
        ans += "\t" + format("Moves") + ":" + "[\n";

        for (int i=0; i<(int)moves.size(); i++) {
            ans += "\t\t" + format(moves[i]);
            if (i+1 < (int) moves.size())    ans += ',';
            ans += "\n";
        }


        ans += "\t]\n";
        ans += "}\n";
        return ans;
    }
} history;

/**
 * result is 0 if first player wins, 
 * 1 if second player wins,
 * 2 if draw
*/	
vector<string> playerName = {"one", "two"};
void writeMatchResult (int result, string reason) {
	if (result == 2) {
        history.result = "Draw";
    }
	else if (result == 0) {
        history.result = "Win";
    }
	else if (result == 1) {
        history.result = "Loss";
    }
    history.reason = reason;

    ofstream jsonfile("matchhistory.json", ofstream::out);
    if (!jsonfile) {
        cout<<"error";
        cerr<<"Can not open log file"<<endl;
        exit(0);
    }
    jsonfile<<history.JSON()<<endl;
    jsonfile.close();
    cout<<"end"<<endl;
	exit(0);
}

void communicateWithPlayer(int player, gameState &currentState) {
	assert(currentState.playerToMove() == player);

	//Receive status from mediator
	string status, playerMove;
	getline(cin, status);
	if (status == "timeout") {
		int winner = (player == 0 ? 1: 0);
		writeMatchResult(winner, "Player " + playerName[player] + " timed out.");
		return;
	}
	else if (status == "ok") {
		//Status ok, receive player move
		getline(cin, playerMove);
        history.moves.push_back(playerMove);
		bool valid = currentState.apply(playerMove);

		if (valid) {
            string reason;
			int result = currentState.result(reason);
			assert(-1 <= result && result <= 2);

			//Game has a result
			if (result != -1) {
				writeMatchResult(result,  reason);
			}
			else {
                cout << "ok" <<endl;
				cout << playerMove << endl;
			}
			return;
		}
		else {
			int winner = (player == 0 ? 1: 0);
			writeMatchResult(winner, "Player " + playerName[player] + " made an Invalid Move.");
			return;
		}
	}
	else {
		assert("unrecognized message" && false);
		return;
	}
}

int main() {
	gameState currentState = gameState::initialState();
	cout<<gameState::initMessage(0)<<endl;
	cout<<gameState::initMessage(1)<<endl;

    history.initialState = currentState;

	while(true) {		
		communicateWithPlayer(0, currentState);
		communicateWithPlayer(1, currentState);
	}
}

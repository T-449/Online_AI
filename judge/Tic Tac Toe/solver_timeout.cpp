#include<bits/stdc++.h>
#include <unistd.h>
using namespace std;

string board[3] = {
    "...",
    "...",
    "..."
};

void Set(int x, int y, char c) {
    assert(0<=x && x<=2 && 0<=y && y<=2 && board[x][y] == '.');
    board[x][y] = c;
}

void opMove() {
    int x, y;
    cin>>x>>y;
    Set(x, y, 'O');
}

void myMove() {
    for (int i=0; i<3; i++)
        for (int j=0; j<3; j++)
            if (board[i][j] == '.') {
                Set(i, j, 'X');
                cout<<i<<" "<<j<<endl;
                return;
            }
}


int main() {
    int playerId;
    cin>>playerId;

    int turn = 0;
    while (true) {
        if (turn == playerId)   myMove();
        else                    opMove();
        turn = !turn;
	sleep(3);
    }
}

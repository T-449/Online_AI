#include<bits/stdc++.h>
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

mt19937 rng(time(0));
void myMove() {
    while (true) {
        int x = rng()%3;
        int y = rng()%3;
        cout<<x<<" "<<y<<endl;
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
    }
}

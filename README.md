# Python Chess AI

First, run the program and you will immediately
be prompted for a move. The way our board is set up is in an ascii-board format. It is an 8x8 grid that either shows a dot, which represents an empty square, a
lowercase letter, which represents a black piece, or an uppercase letter which represents
a white piece. For the letters “R” represents the rook, “N” the knight, “B” the bishop, “Q”
the queen, “K” the king, and “P” the pawn. In chess the board squares are labeled based
on the position of white, where the vertical axis is labeled with numbers and the horizontal
axis is labeled with letters. So, the “R” on the bottom left of figure 3 would be the white
rook at “A1” and the “R” at the bottom right would be the white rook at “H1”. Another
example would be that black’s king, the lowercase k, would be on square “E8”. To begin
play you will be prompted to enter a move, you need to write the square of the piece you
want to move followed by the square of the piece you want to move to. For example, if
you wanted to move black’s king forward, you would enter “e8e7”. This represents “move
the piece on E8 to E7”, if this is an illegal move you will be prompted to make a different
one, if not, a new board will be printed on the screen with your move and the AI’s move as
well. This will continue until there is a draw or a checkmate.

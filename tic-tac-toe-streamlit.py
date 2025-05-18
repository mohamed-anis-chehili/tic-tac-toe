import streamlit as st
import numpy as np
import time

# Set page configuration
st.set_page_config(
    page_title="Tic Tac Toe with AI",
    page_icon="🎮",
    layout="centered"
)

# Initialize session state variables if they don't exist
if 'board' not in st.session_state:
    st.session_state.board = np.full((3, 3), "", dtype=str)
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'winner' not in st.session_state:
    st.session_state.winner = None
if 'human' not in st.session_state:
    st.session_state.human = 'X'
if 'computer' not in st.session_state:
    st.session_state.computer = 'O'
if 'current_turn' not in st.session_state:
    st.session_state.current_turn = 'X'  # X always starts
# Add a state to prevent multiple clicks during computer's turn
if 'waiting_for_computer' not in st.session_state:
    st.session_state.waiting_for_computer = False

# Helper functions for game logic
def check_winner_for_player(board, player):
    # Check rows
    for i in range(3):
        if np.all(board[i, :] == player):
            return True
    
    # Check columns
    for i in range(3):
        if np.all(board[:, i] == player):
            return True
    
    # Check diagonals
    if board[0, 0] == board[1, 1] == board[2, 2] == player:
        return True
    if board[0, 2] == board[1, 1] == board[2, 0] == player:
        return True
    
    return False

def is_board_full(board):
    return not np.any(board == "")

def minimax(board, depth, is_maximizing):
    # Terminal conditions
    if check_winner_for_player(board, st.session_state.computer):
        return 10 - depth
    elif check_winner_for_player(board, st.session_state.human):
        return depth - 10
    elif is_board_full(board):
        return 0
    
    if is_maximizing:
        # Computer's turn (maximizing)
        best_score = float("-inf")
        for i in range(3):
            for j in range(3):
                if board[i, j] == "":
                    board_copy = board.copy()
                    board_copy[i, j] = st.session_state.computer
                    score = minimax(board_copy, depth + 1, False)
                    best_score = max(score, best_score)
        return best_score
    else:
        # Human's turn (minimizing)
        best_score = float("inf")
        for i in range(3):
            for j in range(3):
                if board[i, j] == "":
                    board_copy = board.copy()
                    board_copy[i, j] = st.session_state.human
                    score = minimax(board_copy, depth + 1, True)
                    best_score = min(score, best_score)
        return best_score

def get_computer_move(board):
    best_score = float("-inf")
    best_move = None
    
    for i in range(3):
        for j in range(3):
            if board[i, j] == "":
                board_copy = board.copy()
                board_copy[i, j] = st.session_state.computer
                score = minimax(board_copy, 0, False)
                
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
    
    return best_move

def handle_click(row, col):
    # Ignore if game is over, cell is already filled, or waiting for computer
    if (st.session_state.game_over or 
        st.session_state.board[row, col] != "" or 
        st.session_state.waiting_for_computer):
        return
    
    # Human move
    st.session_state.board[row, col] = st.session_state.human
    
    # Check if human wins
    if check_winner_for_player(st.session_state.board, st.session_state.human):
        st.session_state.game_over = True
        st.session_state.winner = "You"
        return
    
    # Check for draw
    if is_board_full(st.session_state.board):
        st.session_state.game_over = True
        st.session_state.winner = "Draw"
        return
    
    # Set waiting flag to prevent multiple clicks
    st.session_state.waiting_for_computer = True
    
    # Computer's turn
    st.session_state.current_turn = st.session_state.computer
    
    # Rerun to update the UI
    st.rerun()

def computer_move():
    if st.session_state.game_over:
        st.session_state.waiting_for_computer = False
        return
    
    # Get computer's move using minimax
    move = get_computer_move(st.session_state.board)
    
    if move:
        row, col = move
        # Update the board with computer's move
        st.session_state.board[row, col] = st.session_state.computer
        
        # Check if computer wins
        if check_winner_for_player(st.session_state.board, st.session_state.computer):
            st.session_state.game_over = True
            st.session_state.winner = "Computer"
            
        # Check for draw
        elif is_board_full(st.session_state.board):
            st.session_state.game_over = True
            st.session_state.winner = "Draw"
    
    # Switch back to human and reset waiting flag
    st.session_state.current_turn = st.session_state.human
    st.session_state.waiting_for_computer = False

def reset_game():
    st.session_state.board = np.full((3, 3), "", dtype=str)
    st.session_state.game_over = False
    st.session_state.winner = None
    st.session_state.current_turn = st.session_state.human
    st.session_state.waiting_for_computer = False

# Main app layout
st.title("Welcome to my Ai playing room")

# Add game instructions and info
with st.expander("How to Play", expanded=False):
    st.write("""
    1. You play as X, the AI plays as O
    2. Click on any empty cell to make your move
    3. The AI uses the minimax algorithm to make optimal moves
    4. Try to get three X's in a row to win!
    """)

# Game status
status_container = st.container()

# Game board
board_container = st.container()

# Create the 3x3 grid of buttons for the game board
with board_container:
    # Custom CSS to create a fixed 3x3 grid that scales as a unit
    st.markdown("""
    <style>
    /* Center the game board */
    .board-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 0 auto;
        width: 100%;
        max-width: 400px;
    }
    
    /* Main game board - fixed aspect ratio wrapper */
    .game-board {
        position: relative;
        width: 100%;
        padding-bottom: 100%; /* Creates a perfect square */
    }
    
    /* Board grid container */
    .board-grid {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        grid-template-rows: 1fr 1fr 1fr;
        gap: 6px;
        background-color: rgba(0, 0, 0, 0.1);
        padding: 6px;
        border-radius: 8px;
    }
    
    /* Override Streamlit's button styling to ensure proper grid */
    .ttt-cell {
        width: 100%;
        height: 100%;
        margin: 0 !important;
        padding: 0 !important;
        position: relative;
    }
    
    .ttt-cell > div {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
    }
    
    /* Style the buttons to fill the cells completely */
    .ttt-cell button {
        width: 100% !important;
        height: 100% !important;
        margin: 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: min(5vw, 24px) !important;
        font-weight: bold !important;
        padding: 0 !important;
        border-radius: 4px !important;
        background-color: white;
    }
    
    /* Hide default Streamlit elements that might break layout */
    .element-container:has(.ttt-cell) {
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* Style X and O marks */
    .mark-x {
        color: #FF4B4B !important;
    }
    
    .mark-o {
        color: #4B70FF !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Create fixed-ratio container for the game board
    st.markdown('<div class="board-container"><div class="game-board"><div class="board-grid">', unsafe_allow_html=True)
    
    # Create board using raw HTML to completely control layout
    for i in range(3):
        for j in range(3):
            cell_value = st.session_state.board[i, j]
            button_label = cell_value if cell_value else " "
            
            # Determine if cell should be disabled
            disabled = (st.session_state.game_over or 
                         cell_value != "" or 
                         st.session_state.waiting_for_computer)
            
            # Add special styling for X and O
            mark_class = ""
            if cell_value == "X":
                mark_class = "mark-x"
            elif cell_value == "O":
                mark_class = "mark-o"
            
            # Create the cell
            st.markdown(f'<div class="ttt-cell">', unsafe_allow_html=True)
            if st.button(button_label, key=f"cell_{i}_{j}", disabled=disabled, 
                         help=f"Cell position [{i},{j}]"):
                handle_click(i, j)
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Close the board container tags
    st.markdown('</div></div></div>', unsafe_allow_html=True)

# Computer's move (occurs after human's move)
if (st.session_state.current_turn == st.session_state.computer and 
    st.session_state.waiting_for_computer and 
    not st.session_state.game_over):
    with status_container:
        with st.spinner("Computer is thinking..."):
            # Add a small delay to show the "thinking" state
            time.sleep(0.7)
            computer_move()
    
    # Rerun once to update the UI after the computer's move
    st.rerun()

# Display game status
with status_container:
    if st.session_state.game_over:
        if st.session_state.winner == "You":
            st.success("🎉 You win! 🎉")
        elif st.session_state.winner == "Computer":
            st.error("Computer wins!")
        else:
            st.info("It's a draw!")
    else:
        if st.session_state.waiting_for_computer:
            st.warning("Computer is making a move...")
        else:
            st.info("Your turn (X)")

# Reset button
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    reset_disabled = st.session_state.waiting_for_computer
    if st.button("New Game", key="reset", disabled=reset_disabled):
        reset_game()
        st.rerun()

import streamlit as st
import numpy as np
import time

# Set page configuration
st.set_page_config(
    page_title="Tic Tac Toe with AI",
    page_icon="🎮",
    layout="centered"
)

# Initialize session state variables
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
    st.session_state.current_turn = 'X'
if 'processing' not in st.session_state:  # New processing state
    st.session_state.processing = False

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
    if check_winner_for_player(board, st.session_state.computer):
        return 10 - depth
    elif check_winner_for_player(board, st.session_state.human):
        return depth - 10
    elif is_board_full(board):
        return 0
    
    if is_maximizing:
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
    # Prevent interaction during processing or invalid moves
    if (st.session_state.processing or 
        st.session_state.game_over or 
        st.session_state.board[row, col] != ""):
        return
    
    st.session_state.board[row, col] = st.session_state.human
    
    if check_winner_for_player(st.session_state.board, st.session_state.human):
        st.session_state.game_over = True
        st.session_state.winner = "You"
        return
    
    if is_board_full(st.session_state.board):
        st.session_state.game_over = True
        st.session_state.winner = "Draw"
        return
    
    st.session_state.current_turn = st.session_state.computer
    st.rerun()

def computer_move():
    if st.session_state.game_over:
        return
    
    move = get_computer_move(st.session_state.board)
    
    if move:
        row, col = move
        st.session_state.board[row, col] = st.session_state.computer
        
        if check_winner_for_player(st.session_state.board, st.session_state.computer):
            st.session_state.game_over = True
            st.session_state.winner = "Computer"
            return
        
        if is_board_full(st.session_state.board):
            st.session_state.game_over = True
            st.session_state.winner = "Draw"
            return
    
    st.session_state.current_turn = st.session_state.human

def reset_game():
    st.session_state.board = np.full((3, 3), "", dtype=str)
    st.session_state.game_over = False
    st.session_state.winner = None
    st.session_state.current_turn = st.session_state.human
    st.session_state.processing = False  # Reset processing state

# Main app layout
st.title("Tic Tac Toe with Minimax AI")

with st.expander("How to Play", expanded=False):
    st.write("""
    1. You play as X, the AI plays as O
    2. Click on any empty cell to make your move
    3. The AI uses the minimax algorithm to make optimal moves
    4. Try to get three X's in a row to win!
    """)

status_container = st.container()
board_container = st.container()

with board_container:
    cols = st.columns([1, 1, 1])
    
    st.markdown("""
    <style>
    .stButton > button {
        width: 100%;
        height: 80px;
        font-size: 24px !important;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)
    
    for i in range(3):
        cols = st.columns([1, 1, 1])
        for j in range(3):
            with cols[j]:
                cell_value = st.session_state.board[i, j]
                button_label = cell_value if cell_value else " "
                
                # Disable buttons during processing or invalid moves
                disabled = (st.session_state.processing or 
                           st.session_state.game_over or 
                           cell_value != "")
                
                if st.button(button_label, 
                            key=f"cell_{i}_{j}", 
                            disabled=disabled):
                    handle_click(i, j)

if (st.session_state.current_turn == st.session_state.computer and 
    not st.session_state.game_over):
    st.session_state.processing = True  # Start processing
    with status_container:
        with st.spinner("Computer is thinking..."):
            time.sleep(0.5)
            computer_move()
    st.session_state.processing = False  # End processing
    st.rerun()

with status_container:
    if st.session_state.game_over:
        if st.session_state.winner == "You":
            st.success("🎉 You win! 🎉")
        elif st.session_state.winner == "Computer":
            st.error("Computer wins!")
        else:
            st.info("It's a draw!")
    else:
        if st.session_state.current_turn == st.session_state.human:
            st.info("Your turn (X)")
        else:
            st.warning("Computer's turn (O)")

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    # Disable reset button during processing
    if st.button("New Game", 
                key="reset", 
                disabled=st.session_state.processing):
        reset_game()
        st.rerun()

with st.expander("How to Deploy This App", expanded=False):
    st.write("""
    To deploy this Tic Tac Toe game online:
    
    1. **Save this code** in a file named `app.py`
    
    2. **Create a requirements.txt file** with:
       ```
       streamlit
       numpy
       ```
    
    3. **Deploy using Streamlit Cloud**:
       - Visit https://streamlit.io/cloud
       - Create a free account
       - Connect your GitHub repository
       - Select the repository with your app
       - Deploy in just a few clicks!
    """)

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
if 'waiting_for_computer' not in st.session_state:
    st.session_state.waiting_for_computer = False
if 'last_action_time' not in st.session_state:
    st.session_state.last_action_time = time.time()

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
    # Ignore clicks if:
    # 1. Game is over
    # 2. Cell is already filled
    # 3. Waiting for computer's turn
    # 4. Action debounce (prevent double-clicks)
    current_time = time.time()
    time_since_last_action = current_time - st.session_state.last_action_time
    
    if (st.session_state.game_over or 
        st.session_state.board[row, col] != "" or 
        st.session_state.waiting_for_computer or
        time_since_last_action < 0.5):  # Debounce time in seconds
        return
    
    # Update last action time
    st.session_state.last_action_time = current_time
    
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
    
    # Set waiting flag to prevent multiple actions
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
    st.session_state.last_action_time = time.time()  # Reset action timer

def reset_game():
    st.session_state.board = np.full((3, 3), "", dtype=str)
    st.session_state.game_over = False
    st.session_state.winner = None
    st.session_state.current_turn = st.session_state.human
    st.session_state.waiting_for_computer = False
    st.session_state.last_action_time = time.time()

# Main app layout
st.title("Tic Tac Toe with Minimax AI")

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

# Apply custom CSS for a consistent grid layout
with board_container:
    st.markdown("""
    <style>
    /* Main game container */
    .ttt-container {
        width: 100%;
        max-width: 350px;
        margin: 0 auto;
        padding: 10px;
        box-sizing: border-box;
    }
    
    /* Game board - always maintains square aspect ratio */
    .ttt-board {
        position: relative;
        width: 100%;
        padding-bottom: 100%; /* Makes it a perfect square */
        background-color: #eee;
        border-radius: 10px;
        overflow: hidden;
    }
    
    /* Grid layout */
    .ttt-grid {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        display: grid;
        grid-template-columns: 33.333% 33.333% 33.333%;
        grid-template-rows: 33.333% 33.333% 33.333%;
        gap: 2px;
        background-color: #999;
        padding: 2px;
    }
    
    /* Cell styling */
    .ttt-cell {
        position: relative;
        width: 100%;
        height: 100%;
        background-color: white;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    /* Fix Streamlit button container */
    div.stButton {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        margin: 0;
        padding: 0;
    }
    
    /* Individual button styling */
    div.stButton > button {
        width: 100% !important;
        height: 100% !important;
        border-radius: 0 !important;
        font-size: min(8vw, 36px) !important;
        font-weight: bold !important;
        margin: 0 !important;
        padding: 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        background-color: white !important;
    }
    
    /* Fix alignment issues */
    div.stButton div {
        width: 100%;
        height: 100%;
    }
    
    /* X and O styling */
    div.stButton > button:has(span:contains("X")) {
        color: #FF4B4B !important;
    }
    
    div.stButton > button:has(span:contains("O")) {
        color: #4B70FF !important;
    }
    
    /* Hide extra padding in containers */
    div[data-testid="column"] {
        padding: 0 !important;
    }
    
    div[data-testid="stVerticalBlock"] {
        gap: 0 !important;
    }
    
    /* Center the status text */
    .status-text {
        text-align: center;
        margin: 15px 0;
    }
    
    /* Center the reset button */
    .reset-container {
        display: flex;
        justify-content: center;
        margin: 15px 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Create the game board with fixed square aspect ratio
    st.markdown('<div class="ttt-container"><div class="ttt-board"><div class="ttt-grid">', unsafe_allow_html=True)
    
    # Create each cell in the grid
    for i in range(3):
        for j in range(3):
            cell_value = st.session_state.board[i, j]
            button_label = cell_value if cell_value else " "
            
            # Determine if cell should be disabled
            disabled = (st.session_state.game_over or 
                        cell_value != "" or 
                        st.session_state.waiting_for_computer)
            
            # Create the cell with button
            st.markdown(f'<div class="ttt-cell">', unsafe_allow_html=True)
            if st.button(button_label, key=f"cell_{i}_{j}", disabled=disabled):
                handle_click(i, j)
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Close the grid container
    st.markdown('</div></div></div>', unsafe_allow_html=True)

# Computer's move (occurs after human's move)
if (st.session_state.current_turn == st.session_state.computer and 
    st.session_state.waiting_for_computer and 
    not st.session_state.game_over):
    with status_container:
        # Display thinking indicator
        st.markdown('<div class="status-text">', unsafe_allow_html=True)
        with st.spinner("Computer is thinking..."):
            # Add a small delay to show the "thinking" state
            time.sleep(0.7)
            computer_move()
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Rerun once to update the UI after the computer's move
    st.rerun()

# Display game status
with status_container:
    st.markdown('<div class="status-text">', unsafe_allow_html=True)
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
    st.markdown('</div>', unsafe_allow_html=True)

# Reset button
st.markdown('<div class="reset-container">', unsafe_allow_html=True)
reset_disabled = st.session_state.waiting_for_computer
if st.button("New Game", key="reset", disabled=reset_disabled):
    reset_game()
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# Add deployment instructions
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
       
    4. **Alternative Deployment Options**:
       - Render.com (Free tier available)
       - Heroku (Requires credit card)
       - Hugging Face Spaces (Free)
       - Railway.app (Limited free tier)
    """)

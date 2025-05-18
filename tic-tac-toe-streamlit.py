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
    # Ignore if game is over or cell is already filled
    if st.session_state.game_over or st.session_state.board[row, col] != "":
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
    
    # Computer's turn
    st.session_state.current_turn = st.session_state.computer
    
    # Rerun to update the UI
    st.rerun()

def computer_move():
    if st.session_state.game_over:
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
            return
        
        # Check for draw
        if is_board_full(st.session_state.board):
            st.session_state.game_over = True
            st.session_state.winner = "Draw"
            return
    
    # Switch back to human
    st.session_state.current_turn = st.session_state.human

def reset_game():
    st.session_state.board = np.full((3, 3), "", dtype=str)
    st.session_state.game_over = False
    st.session_state.winner = None
    st.session_state.current_turn = st.session_state.human

# Main app layout
st.title("Tic Tac Toe with Minimax AI")

# Center the board and controls
st.markdown("""
<style>
    .main .block-container {
        max-width: 700px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Center all content */
    .stButton, .stSpinner, div[data-testid="stHorizontalBlock"] {
        display: flex;
        justify-content: center;
    }
</style>
""", unsafe_allow_html=True)

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
    # Custom CSS to force the grid to stay as a 3x3 grid even on mobile
    st.markdown("""
    <style>
    /* Grid container */
    .game-grid {
        display: grid;
        grid-template-columns: repeat(3, 100px);
        grid-template-rows: repeat(3, 100px);
        gap: 5px;
        justify-content: center;
        margin: 0 auto;
    }
    
    /* Grid cell */
    .grid-cell {
        width: 100px;
        height: 100px;
        display: flex;
        justify-content: center;
        align-items: center;
        background-color: #f0f2f6;
        border-radius: 4px;
        font-size: 40px;
        font-color: white;
        font-weight: bold;
        cursor: pointer;
    }
    
    .grid-cell.disabled {
        cursor: not-allowed;
        opacity: 0.8;
    }
    
    .grid-cell.x {
        color: #FF4B4B;
    }
    
    .grid-cell.o {
        color: #0068C9;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Container for our custom grid
    html_grid = '<div class="game-grid">'
    
    # Generate the cells
    for i in range(3):
        for j in range(3):
            cell_value = st.session_state.board[i, j]
            cell_class = ""
            
            if cell_value == "X":
                cell_class = " x"
            elif cell_value == "O":
                cell_class = " o"
            
            if cell_value != "" or st.session_state.game_over:
                cell_class += " disabled"
                
            cell_id = f"cell_{i}_{j}"
            cell_content = cell_value if cell_value else "&nbsp;"
            
            html_grid += f'<div class="grid-cell{cell_class}" id="{cell_id}" ' + \
                        f'onclick="handleCellClick({i}, {j})">{cell_content}</div>'
    
    html_grid += '</div>'
    
    # JavaScript to handle clicks
    js_code = """
    <script>
    function handleCellClick(row, col) {
        // Use session_state to communicate back to Streamlit
        const queryString = new URLSearchParams({
            row: row,
            col: col
        }).toString();
        
        window.parent.postMessage({
            type: "streamlit:setComponentValue",
            value: queryString
        }, "*");
    }
    </script>
    """
    
    # Combine HTML and JavaScript
    st.markdown(html_grid + js_code, unsafe_allow_html=True)
    
    # Hidden placeholder to capture clicks
    click_placeholder = st.empty()
    
    # Temporary solution: Keep the original buttons but make them transparent
    # They're necessary for state management while we implement the custom grid
    st.markdown("""
    <style>
    .hidden-buttons button {
        position: absolute;
        opacity: 0;
        pointer-events: none;
    }
    </style>
    """, unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="hidden-buttons">', unsafe_allow_html=True)
        for i in range(3):
            cols = st.columns(3)
            for j in range(3):
                with cols[j]:
                    if st.button(" ", key=f"button_{i}_{j}"):
                        handle_click(i, j)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Create a manual grid selection system with a form
    with st.form(key="grid_form"):
        st.write("Select a cell to make your move:")
        col1, col2 = st.columns(2)
        with col1:
            row = st.selectbox("Row:", [1, 2, 3], key="row_select") - 1
        with col2:
            col = st.selectbox("Column:", [1, 2, 3], key="col_select") - 1
        
        submit = st.form_submit_button("Make Move")
        if submit and not st.session_state.game_over and st.session_state.board[row, col] == "":
            handle_click(row, col)

# Computer's move (occurs after human's move)
if st.session_state.current_turn == st.session_state.computer and not st.session_state.game_over:
    with status_container:
        with st.spinner("Computer is thinking..."):
            # Add a small delay to show the "thinking" state
            time.sleep(0.5)
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
        if st.session_state.current_turn == st.session_state.human:
            st.info("Your turn (X)")
        else:
            st.warning("Computer's turn (O)")

# Reset button
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("New Game", key="reset"):
        reset_game()
        st.rerun()

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

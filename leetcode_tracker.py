import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
import colorsys

# Persistent storage file
DATA_FILE = 'leetcode_challenge_data.json'

class LeetCodeTracker:
    def __init__(self):
        self.load_data()

    def load_data(self):
        """Load existing data or create default structure."""
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                self.data = json.load(f)
        else:
            self.data = {
                'members': [],
                'problems_solved': {},
                'total_problems': 50,
                'start_date': datetime.now().isoformat(),
                'winners': {}
            }
            self.save_data()

    def save_data(self):
        """Save data to persistent storage."""
        with open(DATA_FILE, 'w') as f:
            json.dump(self.data, f, indent=4)

    def add_member(self, name):
        """Add a new member to the challenge."""
        if name and name not in self.data['members']:
            self.data['members'].append(name)
            self.data['problems_solved'][name] = {
                'count': 0,
                'join_date': datetime.now().isoformat()
            }
            self.save_data()
            return True
        return False

    def remove_member(self, name):
        """Remove a member from the challenge."""
        if name in self.data['members']:
            self.data['members'].remove(name)
            del self.data['problems_solved'][name]
            self.save_data()
            return True
        return False

    def increment_problems(self, name):
        """Increment problems solved for a member."""
        if name in self.data['problems_solved']:
            current_count = self.data['problems_solved'][name]['count']
            total_problems = self.data['total_problems']
            
            # Increment if not completed
            if current_count < total_problems:
                self.data['problems_solved'][name]['count'] += 1
                
                # Check for winner
                if current_count + 1 == total_problems:
                    self.data['winners'][name] = datetime.now().isoformat()
                
                self.save_data()
                return True
        return False
    
    def decrement_problems(self, name):
        """Decrement problems solved for a member."""
        if name in self.data['problems_solved']:
            current_count = self.data['problems_solved'][name]['count']
            
            # Decrement if count is above 0
            if current_count > 0:
                self.data['problems_solved'][name]['count'] -= 1
                
                # Remove from winners if previously a winner
                if name in self.data['winners'] and self.data['problems_solved'][name]['count'] < self.data['total_problems']:
                    del self.data['winners'][name]
                
                self.save_data()
                return True
        return False

    def set_total_problems(self, count):
        """Set the total number of problems for the challenge."""
        self.data['total_problems'] = max(1, count)
        self.save_data()
    
    def reset_challenge(self):
        """Reset entire challenge data."""
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)
        self.data = {
            'members': [],
            'problems_solved': {},
            'total_problems': 50,
            'start_date': datetime.now().isoformat(),
            'winners': {}
        }
        self.save_data()

def interpolate_color(progress):
    """
    Create a smooth color transition from red to green based on progress.
    Progress is a float between 0 and 1.
    """
    # Convert progress to HSL color space for smooth transition
    start_hue = 0  # Red
    end_hue = 120  # Green
    
    # Interpolate hue
    current_hue = start_hue + (end_hue - start_hue) * progress
    
    # Convert HSL to RGB
    rgb = colorsys.hls_to_rgb(current_hue/360, 0.5, 1.0)
    
    # Convert to hex
    return '#{:02x}{:02x}{:02x}'.format(
        int(rgb[0] * 255), 
        int(rgb[1] * 255), 
        int(rgb[2] * 255)
    )

def main():
    st.set_page_config(
        page_title="LeetCode Challenge Tracker",
        page_icon="💻",
        layout="wide"
    )

    # Enhanced Custom CSS for professional and aesthetic look
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
    
    body {
        font-family: 'Inter', sans-serif;
        background-color: #0f1117;
        color: #e6e6e6;
    }
    
    .main {
        background: linear-gradient(135deg, #1e2029 0%, #0f1117 100%);
        padding: 2rem;
    }
    
    .stApp {
        background-color: transparent;
    }
    
    .custom-progress {
        height: 30px !important;
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .stButton>button {
        background-color: #4a4a6a;
        color: white;
        border: none;
        padding: 10px 20px;
        font-size: 18px; /* Increased font size */
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s ease;
        border-radius: 8px;
        width: 100%; /* Full width for sub-columns */
        height: 50px; /* Consistent height */
    }
    
    .stButton>button:hover {
        background-color: #5a5a7a;
        transform: scale(1.05);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    .stTextInput>div>div>input {
        background-color: #1e2029;
        color: #e6e6e6;
        border: 1px solid #4a4a4a;
        border-radius: 8px;
        padding: 10px;
    }
    
    .winner-badge {
        background-color: #ffd700;
        color: #1e2029;
        padding: 10px 15px;
        border-radius: 20px;
        font-weight: 600;
        display: inline-block;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

    # Initialize tracker
    tracker = LeetCodeTracker()

    # Top header with elegant design
    st.markdown("<h1 style='text-align: center; color: #e6e6e6; font-weight: 600;'>LeetCode Challenge Tracker</h1>", unsafe_allow_html=True)

    # Settings column
    col_settings, col_info = st.columns([3, 1])
    
    with col_settings:
        settings_menu = st.radio(
            "Challenge Settings", 
            ["", "Add Members", "Remove Members", "Set Problem Count"], 
            horizontal=True
        )

    # Settings actions (same as before)
    if settings_menu == "Add Members":
        new_member = st.text_input("Enter Member Name")
        if st.button("Add Member"):
            if tracker.add_member(new_member):
                st.success(f"{new_member} added to the challenge!")
            else:
                st.warning("Member already exists or invalid name")

    elif settings_menu == "Remove Members":
        member_to_remove = st.selectbox(
            "Select Member to Remove", 
            [""] + tracker.data['members']
        )
        if st.button("Remove"):
            if tracker.remove_member(member_to_remove):
                st.success(f"{member_to_remove} removed from the challenge")
            else:
                st.warning("Invalid member selection")

    elif settings_menu == "Set Problem Count":
        problem_count = st.number_input(
            "Total Problems", 
            min_value=1, 
            value=tracker.data['total_problems']
        )
        if st.button("Update Problem Count"):
            tracker.set_total_problems(problem_count)
            st.success("Problem count updated!")

    # Challenge Goal Display
    st.markdown(f"**Total Challenge Goal:** {tracker.data['total_problems']} Problems")

    # Winners section with enhanced styling
    if tracker.data['winners']:
        st.markdown("<h2 style='color: #e6e6e6;'>🏆 Challenge Winners</h2>", unsafe_allow_html=True)
        for winner, win_time in tracker.data['winners'].items():
            st.markdown(f"<div class='winner-badge'>🥇 {winner} completed on {datetime.fromisoformat(win_time).strftime('%Y-%m-%d %H:%M')}</div>", unsafe_allow_html=True)

    # Members Progress with custom progress bar
    st.markdown("<h2 style='color: #e6e6e6;'>Member Progress</h2>", unsafe_allow_html=True)
    for member in tracker.data['members']:
        col1, col2, col3 = st.columns([3, 2, 1])
        
        with col1:
            st.text(member)
        
        with col2:
            # Calculate progress percentage
            total_problems = tracker.data['total_problems']
            solved = tracker.data['problems_solved'][member]['count']
            progress_percent = min(1.0, solved / total_problems)
            
            # Custom color gradient progress bar
            color = interpolate_color(progress_percent)
            progress_html = f"""
            <div class='custom-progress' style='
                width: 100%; 
                height: 30px; 
                background-color: #333;
                border-radius: 15px;
                overflow: hidden;
            '>
                <div style='
                    width: {progress_percent * 100}%; 
                    height: 100%; 
                    background-color: {color};
                    transition: width 0.5s ease-in-out;
                '></div>
            </div>
            <div style='text-align: center; margin-top: 5px;'>
                {solved}/{total_problems} Problems
            </div>
            """
            st.markdown(progress_html, unsafe_allow_html=True)
        
        with col3:
            # Create sub-columns for "+" and "-" buttons
            button_col1, button_col2 = st.columns(2)
            
            with button_col1:
                if st.button("+", key=f"increment_{member}"):
                    tracker.increment_problems(member)
                    st.experimental_rerun()
            
            with button_col2:
                if st.button("-", key=f"decrement_{member}"):
                    tracker.decrement_problems(member)
                    st.experimental_rerun()

    # ------------------- Added Reset Button Below -------------------
    st.markdown("---")  # Horizontal line for separation
    st.markdown("<h2 style='color: #e6e6e6;'>🔄 Reset Challenge</h2>", unsafe_allow_html=True)
    
    with st.expander("Click to Reset the Entire Challenge"):
        confirmation = st.checkbox("I confirm I want to reset the entire challenge")
        if st.button("Reset Challenge"):
            if confirmation:
                tracker.reset_challenge()
                st.success("🎉 The challenge has been completely reset!")
                st.experimental_rerun()
            else:
                st.warning("Please confirm to reset the challenge.")
    # -----------------------------------------------------------------

if __name__ == '__main__':
        main()

import streamlit as st
import random

# --- Cognitive Test Setup ---
def run_cognitive_test():
    st.title("📝 Cognitive Assessment Test")
    st.markdown("This is a simplified cognitive test used to assess memory, attention, and executive function.")

    # --- Section 1: Word Recall (Immediate) ---
    words_to_remember = ["Apple", "Table", "Penny", "Moon", "Carpet"]
    st.session_state["words"] = words_to_remember  # Store words for later recall
    st.markdown("### 1. Memorize these words:")
    st.markdown(f"**{', '.join(words_to_remember)}**")
    st.info("You will be asked to recall these later.")

    # --- Section 2: Simple Math Problem ---
    math_question = "What is 15 + 9?"
    user_math = st.text_input(f"### 2. Solve this math problem: {math_question}")
    if user_math:
        st.success("Response recorded!")

    # --- Section 3: Word Recall (Delayed) ---
    st.markdown("### 3. Can you recall the words from earlier?")
    recalled_words = st.text_area("Enter the words you remember (comma-separated):")
    if recalled_words:
        recalled_list = [word.strip().lower() for word in recalled_words.split(",")]
        correct_count = sum(1 for word in words_to_remember if word.lower() in recalled_list)
        st.success(f"You remembered **{correct_count} out of {len(words_to_remember)}** words.")

    # --- Section 4: Clock Drawing Test (Basic) ---
    st.markdown("### 4. What time is shown on this clock?")
    random_time = random.choice(["10:10", "4:45", "7:20"])
    st.image(f"https://fake-clock-images.com/{random_time}.png", caption="Clock Time Test")
    user_time = st.text_input("Enter the time shown on the clock:")

    if user_time:
        st.success("Response recorded!")

    # --- Summary & Results ---
    if st.button("Submit Test"):
        st.success("Test completed! A detailed report will be generated.")
        return {
            "math_answer": user_math,
            "recalled_words": recalled_list,
            "correct_word_count": correct_count,
            "clock_time": user_time
        }
    return None
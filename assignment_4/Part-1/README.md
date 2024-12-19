# **📚 Assignment 4 : Evaluating Llama3 on "Notakto" Game Strategy 🧠**

---

### **📝 Task Overview:**
- **Objective**: Test the performance of the **pretrained Llama3 chat model** on a grid-based **"Notakto" game**.
- **Goal**: Evaluate how well Llama3 can make strategic moves by placing "X"s on a **3x3 or 4x4 grid** while:
  - **Avoiding 3 consecutive "X"s** in any direction (horizontal, vertical, or diagonal) for 3X3 grid (similarly 4 for 4x4 grid).
- **Challenges**: Assess the model’s ability to:
  - Correctly **apply game rules** and **strategy**,
  - Make **valid placements** without forming 3 consecutive "X"s,
  - Adapt its strategy based on changing game conditions.

---

### **👥 Group Members:**
- **Atharva Malji (atmalji)** 👨‍💻
- **Vijay Sunkugari (visunku)** 👩‍💻

---
- 📅 **Date Submitted:** December 15, 2024
- 💡 **Course**: Elements of AI

---

### **⚠️ Notes:**

- **📜 Final Summary**: For the **final experiment summary**, scroll to the **end** of the notebook. 📚
  
- **😅 Fun but Frustrating**: It was a **fun** assignment, but definitely **tiring** and at times **frustrating** when the LLM kept getting stuck on simple moves. 😤🔄


---


### **📝 Final Conclusion & Summary**

---

### **1. Test Case Performance:**
#### **Q1 (Which test cases does your implementation pass (i.e chooses the winning move) and fail? Does it also pass on a 4x4 board with sequence length of 4 (build a similar test case if required))**

- **Test Case 1**: ✅ **Passed**
- **Test Case 2**: ❌ **Failed**
- **Test Case 3**: ✅ **Passed**
- **Test Case 4**: ❌ **Failed** (No valid move possible) ⛔
- **Test Case 5**: ✅ **Passed** (After prompting) 🤖➡️✅

**Summary:**
- The model **passed 3/5 test cases**.
- **Test Case 4** failed due to **no valid move**.
- **Test Case 5** required prompting as it got stuck in a loop placing "X" on an existing "X". 🌀

---

### **2. Observations on Prompting:**
#### **Q2 How does changing the prompt impact the performance of the model and what changes help the model choose better moves? (Example - when you ask the model to think step by step, etc.)**
#### **🧠 Prompting Challenges:**
- The model **hallucinates** and places "X"s incorrectly, forming **3 consecutive "X"s** when it shouldn't.
- Despite **clear instructions**, the model often **fails to apply game constraints** consistently.

#### **🔄 Improvement with Prompting:**
- After **extensive prompting**, the model sometimes **corrects itself** but **repeats mistakes** once the task is repeated.
  
#### **⚠️ Core Issue:**
- The model **loses track of rules** after making a correct move and **repeatedly misplaces "X"s** or misses valid spots.

---

### **3. Performance on 4x4 Grid:**

#### **Test Results on 4x4 Grid:**
- **Test Case 1**: ✅ **Passed**
- **Test Case 2**: ✅ **Passed**

**Key Insights:**
- In **sparse grids**, the model performs better with **more space** and fewer "X"s, making it easier to avoid invalid lines.
- **Dense grids** present a bigger challenge as **complexity increases**.

---

### **4. Model vs. Random Player:**

#### **Question 3 On a 3x3 board, can your model win against a random player in a game starting with an empty board? or, how many moves does it play before it begins to fail.**

* ⚠️ For a 3 x 3 grid the model starts failing after 2 moves, given the configuration of the board, but does play for more steps on a 4 x 4 grid but thinks that a line of 3 X is a winning state and stops playing after that.
* Initially, the model **avoids lines of 3 "X"s**, but it **misunderstands the win condition** (thinks 3 "X"s ends the game).
* After being corrected, the model **still fails** and places a line of **4 "X"s**, losing the game instead of continuing. ❌

#### **Key Insights:**
1. **Incorrect Game End Condition**: The model **thinks 3 "X"s is a win**, but it’s actually **4 "X"s** that end the game.
2. **Failure to Adjust**: Despite **clear prompts**, it fails to adapt its strategy and continues to **make mistakes**. 🔄

---

### **💡 Key Takeaways & Recommendations:**

1. **Strengths**:
   - The model does well in **sparse grids**, where it can make valid moves without forming a line of 4 "X"s.
   
2. **Weaknesses**:
   - Struggles with **understanding the game’s end condition** (3 "X"s vs. 4 "X"s).
   - Tends to **repeat mistakes**, especially when the grid fills up.

3. **Improvement Areas**:
   - Better **context management** and **long-term strategy** to avoid mistakes.
   - More robust testing in **denser grids** and with more **complex sequences** to evaluate the model's ability to handle higher complexity.

---

### **🚀 Conclusion:**
- The model performs well in **simple, sparse grids** but struggles as complexity increases.
- **Clear prompting** helps, but the model **needs better consistency** and **rule retention** to perform optimally across all scenarios.
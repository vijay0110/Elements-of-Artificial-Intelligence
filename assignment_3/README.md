# ✨ **Visunku-Atmalji-Singsidd Assignment 3** 🎮

## Part 1: **Minimax Algorithm with Alpha-Beta Pruning** 🤖

### How It Works 🛠️

#### `solver` Function 🧩

The `solver` function is responsible for determining and executing the optimal move in a game using the **Minimax algorithm** with **Alpha-Beta pruning**. It orchestrates the process of evaluating possible moves and selecting the best one based on the current board state. Below is a breakdown of the function's operation:

##### **Input Parsing** 📜:
- **Board String Conversion**: The input board, given as a string, is converted into a 2D grid format using the `parse_board_string_to_grid` function. This grid represents the current state of the game where:
  - `'x'` represents a move by the AI.
  - `'.'` represents an empty position.
- **Validation**: The function checks the validity of the board:
  - Ensures that only valid characters (`'.'`, `'x'`) are present.
  - Verifies that the board dimensions match the specified `n` and `m` (number of rows and columns).
  - Checks that the game has not already been completed by calling the `check_game_completion` function.

##### **Initialization** ⚙️:
- **Alpha-Beta Values**: The alpha and beta values are initialized to negative and positive infinity, respectively. These values guide the pruning process during Minimax to eliminate unnecessary branches of the decision tree.
- **Depth Limit**: A `depthlimit` is set to limit how deep the Minimax algorithm will search. This prevents excessive computation in large or complex boards.

##### **Evaluating Possible Moves** 🔍:
- **Iterating Through Empty Positions**: The `return_empty_positions` function identifies all the empty positions on the board.
- **Simulating Moves**: For each empty position, a simulated move is made by placing an 'x' temporarily on the board.
- **Minimax Evaluation**: After placing the 'x', the Minimax algorithm is invoked to evaluate the resulting board state, considering potential future moves up to the specified depth limit.
- **Undoing the Move**: After each evaluation, the board is reverted to its original state by removing the temporary 'x' from the simulated position.

##### **Selecting the Best Move** 🏆:
- **Comparing Evaluation Scores**: After evaluating all potential moves, the function compares their evaluation scores and selects the move with the highest score.
- **Handling Ties**: If multiple moves yield the same evaluation score, one is chosen randomly to introduce variability and prevent the AI from being too predictable.

##### **Executing the Best Move** 🖱️:
- **Applying the Move**: The selected best move is then applied to the board by placing an 'x' at the chosen position.
- **Fallback Mechanism**: In case no best move is found (which is unlikely), a random empty position is selected as a fallback.

##### **Returning the Updated Board** 🔄:
- The function returns the updated board state after executing the best move.

---

#### `minimax` Function 🎲

The `minimax` function is the core of the decision-making process. It evaluates the current board state by recursively simulating future moves for both the maximizing player (AI) and the minimizing player (opponent). Here’s how it works:

##### **Base Cases** ⏸️:
- **Losing State**: If the board is in a losing state for the opponent, the function assigns a high positive score if it's the maximizing player’s turn, or a negative score if it's the minimizing player’s turn.
- **Draw State**: If no empty positions remain, the function returns a score of 0, indicating a draw.
- **Depth Limit**: When the recursion depth reaches zero, the function uses the `evaluate_board` function to return a heuristic score of the current board state.

##### **Recursive Evaluation** 🔄:
- **Maximizing Player (AI)**:
  - **Exploring Moves**: The function explores each possible move for the AI (maximizing player), simulating placing an 'x' at each empty position.
  - **Updating Scores**: It tracks the highest score encountered during the search.
  - **Alpha-Beta Pruning**: The function prunes branches where further exploration would not affect the final decision (i.e., if `beta <= alpha`).
  
- **Minimizing Player (Opponent)**:
  - **Exploring Moves**: The function evaluates moves for the opponent (minimizing player) by simulating placing an 'x' on the board and recursively calling itself to evaluate each state.
  - **Updating Scores**: It tracks the lowest score encountered.
  - **Alpha-Beta Pruning**: Similar to the maximizing player, it prunes branches based on the alpha-beta values.

##### **Alpha-Beta Pruning** ✂️:
- **Purpose**: Alpha-Beta pruning reduces the number of nodes the Minimax algorithm needs to evaluate by eliminating branches that are guaranteed to be suboptimal.
- **Implementation**: As the tree is traversed, the algorithm maintains and updates alpha and beta values, skipping unnecessary branches if they won't affect the final result.

##### **Heuristic Evaluation** 🔍:
- **Depth Limitation Impact**: When the depth limit is reached, the algorithm uses a heuristic evaluation to estimate the board’s favorability based on the current configuration of 'x' marks.
- **Efficiency**: This prevents the algorithm from exhaustively searching all possible moves in deeply nested game states, thus balancing computation time and decision quality.

---

### Optimizations ⚡

#### **Alpha-Beta Pruning** 🔒:
- **Functionality**: The pruning significantly reduces the number of branches explored by Minimax, speeding up the decision-making process, especially when the search tree is deep.
- **Benefit**: This optimization enhances the algorithm’s performance, especially for larger boards or more complex game states.

#### **Heuristic Evaluation Function** 🧠:
- **Functionality**: Instead of simulating every possible future move, the evaluation function estimates the favorability of the board by considering potential sequences of 'x' marks (winning lines).
- **Benefit**: This approach reduces the computational cost, allowing the AI to make decisions efficiently even with larger grids.

#### **Depth Limitation (`depthlimit`)** ⏳:
- **Functionality**: The search depth is limited to a predefined value to prevent excessive computation in large or complex games.
- **Benefit**: The depth limit ensures that the solver remains responsive, balancing between thoroughness and speed.

#### **Random Move Selection in Ties** 🎲:
- **Functionality**: In cases where multiple moves have identical evaluation scores, the solver randomly selects one of them to introduce unpredictability.
- **Benefit**: This prevents the AI from being too deterministic and encourages exploration of different strategic paths.

---

### Performance Notes 🚀

- The algorithm uses a maximum search depth to balance performance and decision quality. For larger boards or more complex game states, you may need to increase the `depthlimit` for more accurate results.

### Challenges faced 🚀

- One of the challenges faced was determining the appropriate weights and the length of vector 𝑥 that was generated. Additionally, designing a robust evaluation function or heuristic to distinguish between different neutral moves was also a significant challenge.



---

## Part 2: **Part-of-Speech Tagging with HMM and Simplified Models** 🏷️

### Overview 📚

This implementation focuses on Part-of-Speech (POS) tagging using two main models:
1. **Simplified Model** 📝: A basic model that assigns the most frequent POS tag for each word based on training data.
2. **Hidden Markov Model (HMM)** 🔍: A probabilistic model using the Viterbi algorithm for optimal sequence tagging.

The provided code includes a `Solver` class that:
- Trains the POS tagging model on a given dataset.
- Computes posterior probabilities for a sentence using both models.
- Uses the trained model to tag new sentences with their respective POS labels.

---

### `Solver` Class 🧑‍🏫

The `Solver` class implements the main functionality of the POS tagging system. Below is a breakdown of its key methods and their roles:

#### **`__init__` Method** 🏗️
Initializes the `Solver` object and sets up required variables:

- **`trans`**: Transition probabilities between POS tags.
- **`emit`**: Emission probabilities of words given a POS tag.
- **`data`**: Stores frequency counts of words for each POS tag.
- **`total_words`**: Total number of words in the training dataset.
- **`states`**: List of possible POS tags.

```python
def __init__(self):
    self.trans = None
    self.emit = None
    self.data = None
    self.total_words = 0
    self.states = ["ADJ", "ADV", "ADP", "CONJ", "DET", "NOUN", "NUM", "PRON", "PRT", "VERB", "X", "."]
```

#### **`posterior` Method** 🔢
Computes the log of the posterior probability of a sentence given a particular model and a list of POS labels. It uses either the **Simplified** or **HMM** model.

```python
def posterior(self, model, sentence, label):
    if model == "Simple":
        return self.simplified(sentence, posterior=True, list_of_labels=label)
    elif model == "HMM":
        return self.hmm_viterbi(sentence, posterior=True, list_of_labels=label)
    else:
        print("Unknown algo!")
```

#### **`process_word` Method** 🧽
Preprocesses a word by removing

 its possessive suffix (i.e., `"'s"`), if applicable.

```python
def process_word(self, word):
    if word[-2:] == "'s":
        word = word[:-2]
    return word
```

#### **`train` Method** 📊
Trains the POS tagging model on the provided training data. It calculates:
- **Transition probabilities** between consecutive POS tags.
- **Emission probabilities** for each word given a POS tag.
- **Initial probabilities** for each POS tag.

```python
def train(self, data):
    occurances = {}
    total_words = 0
    init = {"ADJ": 0, "ADV": 0, "ADP": 0, "CONJ": 0, "DET": 0, "NOUN": 0, "NUM": 0, "PRON": 0, 
            "PRT": 0, "VERB": 0, "X": 0, ".": 0}
    
    trans = {i: {j: 0 for j in init} for i in init}
    emit = dict()
    
    # Process training data and calculate probabilities
    for sentence, labels in data:
        for i in range(len(sentence)):
            word_in_question = sentence[i]
            word_in_question = self.process_word(word_in_question)
            label = labels[i].upper()

            if i < len(sentence) - 1:
                next_label = labels[i+1].upper()

            trans[label][next_label] += 1
            
            if word_in_question not in occurances:
                occurances.update({word_in_question: {"ADJ": 0, "ADV": 0, "ADP": 0, "CONJ": 0,
                                                      "DET": 0, "NOUN": 0, "NUM": 0, "PRON": 0, 
                                                      "PRT": 0, "VERB": 0, "X": 0, ".": 0, "TOTAL": 0}})
                
            occurances[word_in_question][label.upper()] += 1
            init[label.upper()] += 1
            occurances[word_in_question]["TOTAL"] += 1
            total_words += 1

    # Normalize transition probabilities
    for label_1 in init:
        for label_2 in trans[label.upper()]:
            trans[label_1][label_2] = trans[label_1][label_2] / init[label_1]

    # Normalize emission probabilities
    for label in init:
        emit.update({label: {word: (occurances[word][label]) / init[label] for word in occurances}})

    # Normalize initial probabilities
    for label in init:
        init[label] = init[label] / total_words

    self.trans = trans
    self.emit = emit
    self.init = init
    self.data = occurances
    self.total_words = total_words
```

#### **`simplified` Method** 💡
Assigns POS tags to a sentence based on the most likely tag for each word, using the **Simplified Model**. If the `posterior` flag is set to `True`, it returns the log of the product of the probabilities.

```python
def simplified(self, sentence, posterior=False, list_of_labels=None):
    pred = []
    probabilities = []
    
    for word in sentence:
        word = self.process_word(word)

        if word not in self.data:
            pred.append("X")
            probabilities.append(self.init['X'])
        else:
            occurances = self.data[word]
            likelihoods = [(occurances[state]) / (occurances["TOTAL"]) for state in self.states]
            pred.append(self.states[likelihoods.index(max(likelihoods))])
            probabilities.append(max(likelihoods))

    if posterior:
        return math.log(math.prod(probabilities))
    else:
        return [i.lower() for i in pred]
```

#### **`hmm_viterbi` Method** 🧩
Uses the **Hidden Markov Model (HMM)** and the **Viterbi algorithm** to find the most likely sequence of POS tags for a given sentence. It calculates the probabilities of state transitions and emissions for each word and uses dynamic programming to find the optimal path.

```python
def hmm_viterbi(self, sentence, posterior=False, list_of_labels=None):
    S = len(self.states)
    T = len(sentence)
    
    prob = [[0 for i in range(S)] for j in range(T)]
    prev = [[None for i in range(S)] for j in range(T)]

    sentence = [self.process_word(word) for word in sentence]
    
    # Initialization: compute initial probabilities for the first word
    for s in self.states:
        if sentence[0] not in self.emit[s]:
            prob[0][self.states.index(s)] = 0
        else:
            prob[0][self.states.index(s)] = self.init[s] * self.emit[s][sentence[0]]

    # Recursion: fill in the probabilities for the subsequent words
    for t in range(1, T):
        for s in self.states:
            for r in self.states:
                s_index = self.states.index(s)
                r_index = self.states.index(r)
                if sentence[t] not in self.emit[s]:
                    new_prob = prob[t - 1][r_index] * self.trans[r]['X']
                else:
                    new_prob = prob[t - 1][r_index] * self.trans[r][s] * self.emit[s][sentence[t]]
                if new_prob >= prob[t][s_index]:
                    prob[t][s_index] = new_prob
                    prev[t][s_index] = r

    # Backtrack to find the most likely sequence of POS tags
    path = [None for _ in range(T)]
    probabilities = [0 for _ in range(T)]
    path[T - 1] = self.states[prob[T - 1].index(max(prob[T - 1]))]
    probabilities[T - 1] = max(prob[T - 1])
    
    for t in range(T - 2, -1, -1):
        path[t] = prev[t + 1][self.states.index(path[t + 1])]
        probabilities[t] = max(prob[t])

    if posterior:
        if probabilities[0] == 0:
            return -99
        return math.log(probabilities[0])
    
    return [i.lower() for i in path]
```

#### **`solve` Method** 🧠
The `solve` method is used to tag a sentence using either the **Simplified Model** or the **HMM Model**. It calls either the `simplified` or `hmm_viterbi` function depending on the selected model.

```python
def solve(self, model, sentence):
    if model == "Simple":
        return self.simplified(sentence)
    elif model == "HMM":
        return self.hmm_viterbi(sentence)
    else:
        print("Unknown algo!")
```

### Challenges faced 🚀

To manage unseen words in the training set, we introduced a very small probability value of $10^{(-15)}$, instead of setting the probability to zero. This helped improve accuracy by preventing the model from consistently defaulting to the last POS tag for unknown words.


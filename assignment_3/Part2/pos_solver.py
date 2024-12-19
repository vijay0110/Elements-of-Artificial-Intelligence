###################################
# CS B551 Fall 2024, Assignment #3
#
# Your names and user ids:
#

import random
import math


class Solver:
    # Calculate the log of the posterior probability of a given sentence
    # with a given part-of-speech labeling.
    
    def posterior(self, model, sentence, label):
        # Computes the log of the posterior probability for different models.
        # For the simplified model, only considers the emission probabilities.
        prob_min_emission = pow(10, -15)  # Very small probability for unseen words to avoid zero probability
        if model == "Simple":
            log_sum = 0
            for i in range(len(label)):
                # Add the log probability of the part of speech (POS)
                log_sum += math.log(self.dict_pos[label[i]])
                # Add the log probability of the word given the POS
                if sentence[i] in self.emission_prob[label[i]]:
                    log_sum += math.log(self.emission_prob[label[i]][sentence[i]])
                else:
                    log_sum += math.log(prob_min_emission)  # Handle unseen words with a very low probability
            return log_sum

        elif model == "HMM":
            # Calculate the posterior probability for the HMM model including initial, emission, and transition probabilities
            temp_sum_emission, temp_sum_transition = prob_min_emission, prob_min_emission

            # Handle the initial state of the sentence
            log_initial = math.log(self.initial_prob[label[0]])
            if sentence[0] in self.emission_prob[label[0]]:
                temp_sum_emission = math.log(self.emission_prob[label[0]][sentence[0]])

            final_prob = log_initial + temp_sum_emission

            # Loop through the rest of the sentence and accumulate probabilities
            for i in range(1, len(sentence)):
                if sentence[i] in self.emission_prob[label[i]]:
                    temp_sum_emission = math.log(self.emission_prob[label[i]][sentence[i]])
                else:
                    temp_sum_emission = math.log(prob_min_emission)

                # Consider the transition probability between the current POS and the previous one
                if label[i] in self.transition_prob[label[i - 1]]:
                    temp_sum_transition = math.log(max(self.transition_prob[label[i - 1]][label[i]], prob_min_emission))
                else:
                    temp_sum_transition = math.log(prob_min_emission)

                final_prob += temp_sum_emission + temp_sum_transition
            return final_prob
        else:
            print("Unknown model specified!")

    # Train the model using given data
    def train(self, data):
        # List of all possible parts of speech (POS)
        pos_tags = [
            "adj",
            "adv",
            "adp",
            "conj",
            "det",
            "noun",
            "num",
            "pron",
            "prt",
            "verb",
            "x",
            ".",
        ]

        # Initialize dictionaries to track POS frequencies, word frequencies, and transition counts
        self.dict_pos = {tag: 0 for tag in pos_tags}
        word_pos_count = {tag: {} for tag in pos_tags}
        self.transition_prob = {tag: {next_tag: 0 for next_tag in pos_tags} for tag in pos_tags}
        self.initial_prob = {}

        # Count occurrences for initial POS, transitions, and emissions
        for sentence, tags in data:
            # Count the initial state occurrences
            initial_tag = tags[0]
            self.initial_prob[initial_tag] = self.initial_prob.get(initial_tag, 0) + 1

            # Count POS and word frequencies
            for word, tag in zip(sentence, tags):
                word_pos_count[tag][word] = word_pos_count[tag].get(word, 0) + 1
                self.dict_pos[tag] += 1

            # Count transitions between consecutive POS tags
            for i in range(len(tags) - 1):
                current_tag, next_tag = tags[i], tags[i + 1]
                self.transition_prob[current_tag][next_tag] += 1

        # Normalize initial POS probabilities
        total_initial = sum(self.initial_prob.values())
        for tag in self.initial_prob:
            self.initial_prob[tag] /= total_initial

        # Normalize POS counts to obtain probabilities
        total_pos_count = sum(self.dict_pos.values())
        for tag in self.dict_pos:
            self.dict_pos[tag] /= total_pos_count

        # Normalize transition probabilities
        for tag in self.transition_prob:
            total_transitions = sum(self.transition_prob[tag].values())
            if total_transitions > 0:
                for next_tag in self.transition_prob[tag]:
                    self.transition_prob[tag][next_tag] /= total_transitions

        # Normalize emission probabilities
        self.emission_prob = {}
        for tag in word_pos_count:
            self.emission_prob[tag] = {}
            total_emissions = sum(word_pos_count[tag].values())
            if total_emissions > 0:
                for word in word_pos_count[tag]:
                    self.emission_prob[tag][word] = word_pos_count[tag][word] / total_emissions

    # Functions for each algorithm.

    # For the simplified model, return the POS tag with the highest emission probability for each word
    def simplified(self, sentence):
        predictions = []
        for word in sentence:
            highest_prob = 0.0
            predicted_tag = "noun"
            # Find the POS tag with the highest emission probability for the given word
            for tag in self.emission_prob:
                if word in self.emission_prob[tag]:
                    current_prob = self.emission_prob[tag][word]
                    if current_prob > highest_prob:
                        highest_prob = current_prob
                        predicted_tag = tag
            predictions.append(predicted_tag)
        return predictions

  
    # HMM Viterbi Algorithm

    def hmm_viterbi(self, sentence):
        pos_tags = [
            "adj",
            "adv",
            "adp",
            "conj",
            "det",
            "noun",
            "num",
            "pron",
            "prt",
            "verb",
            "x",
            ".",
        ]

        prob_min_emission = pow(10, -10)
        viterbi_prob, backpointer = self.initialize_viterbi(sentence, pos_tags, prob_min_emission)
        viterbi_prob, backpointer = self.recursion_viterbi(sentence, pos_tags, viterbi_prob, backpointer, prob_min_emission)
        result = self.backtrace_viterbi(sentence, pos_tags, viterbi_prob, backpointer)
        return result

    def initialize_viterbi(self, sentence, pos_tags, prob_min_emission):
        # Dictionary to store probabilities and backtrace paths
        viterbi_prob = [{} for _ in range(len(sentence))]
        backpointer = [{} for _ in range(len(sentence))]

        # Initialization step
        for tag in pos_tags:
            if tag in self.initial_prob:
                initial_prob = self.initial_prob[tag] * self.emission_prob[tag].get(sentence[0], prob_min_emission)
                viterbi_prob[0][tag] = math.log(initial_prob) if initial_prob > 0 else float('-inf')
                backpointer[0][tag] = None

        return viterbi_prob, backpointer

    def recursion_viterbi(self, sentence, pos_tags, viterbi_prob, backpointer, prob_min_emission):
        # Recursion step
        for t in range(1, len(sentence)):
            for tag in pos_tags:
                max_prob = float('-inf')
                best_prev_tag = None
                for prev_tag in pos_tags:
                    if prev_tag in viterbi_prob[t - 1]:
                        transition_prob = max(self.transition_prob[prev_tag].get(tag, 0), prob_min_emission)
                        emission_prob = max(self.emission_prob[tag].get(sentence[t], 0), prob_min_emission)
                        prob = viterbi_prob[t - 1][prev_tag] + math.log(transition_prob) + math.log(emission_prob)

                        if prob > max_prob:
                            max_prob = prob
                            best_prev_tag = prev_tag

                viterbi_prob[t][tag] = max_prob
                backpointer[t][tag] = best_prev_tag

        return viterbi_prob, backpointer

    def backtrace_viterbi(self, sentence, pos_tags, viterbi_prob, backpointer):
        # Termination step
        max_final_prob = float('-inf')
        best_last_tag = None
        for tag in pos_tags:
            if viterbi_prob[-1].get(tag, float('-inf')) > max_final_prob:
                max_final_prob = viterbi_prob[-1][tag]
                best_last_tag = tag

        # Backtrace to find the best path
        result = []
        current_tag = best_last_tag
        for t in range(len(sentence) - 1, -1, -1):
            result.insert(0, current_tag)
            current_tag = backpointer[t][current_tag]

        return result


    # This solve() method is called by label.py, so you should keep the interface the
    #  same, but you can change the code itself. 
    # It should return a list of part-of-speech labelings of the sentence, one
    #  part of speech per word.
    #
    def solve(self, model, sentence):
        if model == "Simple":
            return self.simplified(sentence)
        elif model == "HMM":
            return self.hmm_viterbi(sentence)
        else:
            print("Unknown algo!")


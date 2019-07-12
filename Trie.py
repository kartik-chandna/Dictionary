from collections import Counter
import heapq

class TrieNode:
    def __init__(self):
        self.child = [None for _ in range(26)]
        self.is_end = False
        self.freq = 0
        self.meaning = ''


class Trie:
    def __init__(self):
        self.root = TrieNode()
        self.h = []
        
    def ch2idx(self, c):
        return ord(c)- ord('a')
    
    def insert_word(self, word, meaning):
        temp = self.root
        for i in range(len(word)):
            if not temp.child[self.ch2idx(word[i])]:
                temp.child[self.ch2idx(word[i])] = TrieNode()
            temp = temp.child[self.ch2idx(word[i])]
        temp.is_end = True
        temp.meaning = meaning)
        
    def search_word_util(self, word):
        temp = self.root
        for i in range(len(word)):
            if not temp.child[self.ch2idx(word[i])]:
                return False, 0,0
            temp = temp.child[self.ch2idx(word[i])]
        if not temp.is_end:
            return False, 0,0
        else:
            temp.freq += 1
            if len(self.h) < 5:
                heapq.heappush(self.h, (temp.freq, word))
            elif temp.freq > self.h[0][0]:
                heapq.heappop(self.h)
                heapq.heappush(self.h, (temp.freq, word))
            return True, temp.meaning, temp.freq

    def suggestions_util(self, node, suggest, l):
        if not node:
            return
        if node.is_end:
            suggest.append((node.freq, ''.join(l)))
        for i in range(26):
            if node.child[i]:
                l.append(chr(ord('a')+i))
                self.suggestions_util(node.child[i], suggest, l)
                l.pop()
    
    def suggestions(self, word):
        temp = self.root
        for i in range(len(word)):
            if not temp.child[self.ch2idx(word[i])]:
                print("The longest prefix : " + word[:i])
            temp = temp.child[self.ch2idx(word[i])]
            if not temp:
                break

        if temp:
            print("The longest prefix : " + word)
        ##autocomplete
        suggest = []
        self.suggestions_util(temp, suggest, [])
        suggest = sorted(suggest, reverse = True)
        print("Autocomplete options sorted based on frequency: ")
        for j in range(len(suggest)):
            print(word[:i+1]+ suggest[j][1] + " ---> " + str(suggest[j][0]))
    
    def is_anagram(self, word, word1):
        if Counter(word) == Counter(word1):
            print(word1)

    def trie_search(self, word, temp, l, flag):
        if not temp:
            return
        if temp.is_end:
            if not flag:
                self.edit_distance_util(word,''.join(l))
            else:
                self.is_anagram(word, ''.join(l))
        for i in range(26):
            if temp.child[i]:
                l.append(chr(ord('a')+i))
                self.trie_search(word, temp.child[i], l, flag)
                l.pop()
    
    def edit_distance_util(self, word, word1):
        dp = [[0 for _ in range(len(word1)+1)] for _ in range(len(word)+1)]

        for j in range(1 , len(word1)+1):
            dp[0][j] = j

        for i in range(1 , len(word)+1):
            dp[i][0] = i

        for i in range(1 , len(word)+1):
            for j in range(1 , len(word1)+1):
                if word[i-1] == word1[j-1]:
                    dp[i][j] = dp[i-1][j-1]
                else:
                    dp[i][j] = 1 + min(dp[i-1][j-1], dp[i-1][j], dp[i][j-1])

        if dp[-1][-1] < 3:
            print(word1)

    
    def search_word(self, word):
        f = open("words.txt" , "a+")
        f.write(word + '\n')
        f.close()
        
        b, meaning, freq = self.search_word_util(word)
        if b:
            print("The word entered is in the dictionary")
            print("Mearning : " + meaning)
            print("Frequency : " + str(freq))
        else:
            print("The word entered is not in the dictionary")
            self.suggestions(word)

            print("The anagrams of the word entered : ")
            self.trie_search(word, self.root , [], True)

            print("Words related to the given word if they have maximum 2 errors :")
            self.trie_search(word, self.root , [], False)
            

    def most_searched_words(self):
        print("Top 5 most seached words : ")
        arr = sorted(self.h, reverse=True)
        for i in range(len(arr)):
            print(arr[i][1] + "--->" + str(arr[i][0]))

    def get_history(self):
        print("Previously searched words: ")
        f = open("words.txt" ,"r")
        f1 = f.readlines()
        for word in f1:
            print(word)
        f.close()

def main():
    t = Trie()
    while True:
        print("1. Insert word")
        print("2. Search word")
        print("3. Top 5 most searched words")
        print("4. Get searched history")
        print("Press any other character for exit")
        num = int(input())

        if num not in [1,2,3,4]:
            break
        elif num == 1:
            print("Enter the word to be inserted : ")
            word = input()
            print("Enter the meaning of the word : ")
            mean = input()
            t.insert_word(word.lower(), mean)
        elif num == 2:
            print("Enter the word to be searched : ")
            word = input()
            t.search_word(word.lower())
        elif num == 3:
            t.most_searched_words()
        elif num == 4:
            t.get_history()

if __name__ == "__main__":
    main()
        





                

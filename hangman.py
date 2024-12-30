import random
import tkinter as tk
from tkinter import messagebox
from hangman_words import word_list
from hangman_ui import logo

# 게임 상태 클래스
class HangmanGame:
    def __init__(self):
        self.chosen_word = random.choice(word_list) # hangman_words에서 import한 word_list에서 단어 랜덤 선택
        self.word_length = len(self.chosen_word) # 단어 길이 재기
        self.user_guess = ['_'] * self.word_length # 단어에 맞게 _로 나타냄
        self.guess_set = set() # 사용자가 추측한 알파벳 저장
        self.life = 7 # 사용자에게 부여한 단 7개의 목숨
        self.game_over = False # 게임이 끝났는지 판단하는 플래그

    # 추측한 알파벳 처리하는 함수
    def make_guess(self, guess):
        if guess in self.guess_set: # 이미 추측한 알파벳이라면 아래 멘트 반환
            return "이미 입력한 알파벳입니다. 다른 알파벳을 입력하세요!"
        self.guess_set.add(guess) # 추측한 알파벳 저장

        if guess not in self.chosen_word: # 사용자가 추측한 알파벳이 단어에 없다면 목숨 하나 차감
            self.life -= 1
            if self.life <= 0: # 목숨이 0 이하가 되면 게임 종료
                self.game_over = True # 게임이 끝났는지 판단하는 플래그가 True가 됨
                return f"정답은 {self.chosen_word}였습니다. 아쉽습니다:("
            return "단어 내에 존재하지 않는 철자입니다! 다시 입력하세요."
        
        for idx, letter in enumerate(self.chosen_word): # 추측한 알파벳이 단어에 있다면, 그 자리에 업데이트
            if letter == guess:
                self.user_guess[idx] = letter

        if "_" not in self.user_guess: # 모든 알파벳을 맞히면
            self.game_over = True # 플래그가 True가 되어 게임 종료 후 아래 멘트 반환
            return "정답입니다! 당신은 행맨 고수군요!"
        
        return " ".join(self.user_guess) # 단어의 현재 상태 반환

# GUI 초기화
root = tk.Tk()
root.title("Hangman Game")
root.geometry("800x600")
root.resizable(False, False)



# 게임 상태 객체
game = HangmanGame()

# 텍스트 라벨들

tk.Label(root, text=logo, font=("Courier", 12), justify="left").pack(pady=20) # 행맨 로고 삽입
label_word = tk.Label(root, text=" ".join(game.user_guess), font="Arial 40 bold") # 단어의 현재 상태
label_word.pack(pady=20)
label_lives = tk.Label(root, text=f"남은 목숨: {game.life}", font="Arial 20 bold") # 남은 목숨 수
label_lives.pack(pady=10)
label_message = tk.Label(root, text="", font="Arial 30 bold") # 멘트 출력 형식
label_message.pack(pady=10)


# 알파벳 입력 처리하는 함수
def on_input_change(event):
    guess = entry.get().lower() # 입력한 알파벳을 소문자로 변환함

    if len(guess) != 1 or not guess.isalpha(): # 1개의 알파벳인지 확인함
        label_message.config(text="단 하나의 알파벳만 입력하세요!") # 만약 잘못 입력했다면...
        return

    message = game.make_guess(guess)
    label_word.config(text=" ".join(game.user_guess)) # 추측 결과 업데이트
    label_lives.config(text=f"남은 목숨: {game.life}") # 남은 목숨 업데이트 후
    label_message.config(text=message) # 결과 표시

    if game.game_over: # 게임 종료 후 단어의 현재 상태에 따른 멘트 출력
        if game.life <= 0: # 목숨이 0 이하라면 아래 멘트 출력
            messagebox.showinfo("게임 오버", f"정답은 {game.chosen_word}였습니다. 아쉽습니다 :(")
        else: # 목숨이 0 초과라면 아래 멘트 출력
            messagebox.showinfo("게임 승리", "정답입니다! 당신은 행맨 고수군요!")
        disable_input() # 게임이 종료되었으니 입력 비활성화

# 알파벳 입력창
entry = tk.Entry(root, font="Arial")
entry.pack(pady=20)

# 입력한 내용 제출 버튼
submit_button = tk.Button(root, text="추측하기", command=lambda: on_input_change(None), font="Arial 20 bold")
submit_button.pack(pady=10)

# 게임이 끝나면 버튼이 비활성화 되도록 하는 함수
def disable_input(): 
    entry.config(state="disabled")
    submit_button.config(state="disabled")

# 새 게임 시작하는 함수
def new_game():
    global game
    game = HangmanGame() # 새 게임 객체 생성
    label_word.config(text=" ".join(game.user_guess))
    label_lives.config(text=f"남은 목숨: {game.life}")
    label_message.config(text="")
    entry.config(state="normal")
    submit_button.config(state="normal")

# 새 게임 도전하는 버튼
button_new_game = tk.Button(root, text="새 게임 도전하기", command=new_game, font="Arial 20 bold")
button_new_game.pack(pady=20)

# GUI 실행
root.mainloop()

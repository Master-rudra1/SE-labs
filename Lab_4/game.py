import random
from logic import feedback


class Mastermind:
    def __init__(self, turns=10):
        self.code = [str(random.randint(1, 6)) for _ in range(4)]
        self.history = []
        self.max_turns = turns
        self.turns_left = turns

    def print_board(self):
        if not self.history:
            return
        print("\n--- Guess History ---")
        print(f"{'Turn':<6} {'Guess':<8} {'Exact':<8} {'Partial':<8}")
        print("-" * 32)
        for i, (g, e, p) in enumerate(self.history, 1):
            print(f"{i:<6} {g:<8} {e:<8} {p:<8}")
        print("-" * 32 + "\n")

    def play_round(self):
        print("\nMastermind - Enter 4 digits from 1 to 6 (or 'q' to quit).")
        while self.turns_left > 0:
            self.print_board()
            raw = input(f"[{self.turns_left} turns left] > ").strip()

            if raw.lower() == "q":
                print("Game quit.")
                return False

            if len(raw) != 4 or any(ch not in "123456" for ch in raw):
                print("Invalid input! Please enter exactly four digits from 1 to 6.")
                continue

            guess = list(raw)
            exact, partial = feedback(self.code, guess)
            self.history.append((raw, exact, partial))
            self.turns_left -= 1

            print(f"Feedback -> Exact: {exact} | Partial: {partial}")

            if exact == 4:
                self.print_board()
                print(f"Cracked the code in {self.max_turns - self.turns_left} turn(s)! Congratulations!")
                return True

        print(f"\nGame Over! The secret code was {''.join(self.code)}.")
        return True

    @classmethod
    def select_difficulty(cls):
        print("Select Difficulty Level:")
        print("1. Easy (12 turns)")
        print("2. Medium (10 turns)")
        print("3. Hard (8 turns)")
        choice = input("Enter choice (1/2/3, default 2): ").strip()
        turns_map = {"1": 12, "2": 10, "3": 8}
        return turns_map.get(choice, 10)

    def run(self):
        while True:
            turns = self.select_difficulty()
            game = Mastermind(turns=turns)
            played = game.play_round()
            if not played:
                break
            again = input("\nWould you like to play another game? (y/n): ").strip().lower()
            if again != "y":
                print("Thanks for playing Mastermind!")
                break

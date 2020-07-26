import tkinter as tk
import numpy as np


def ReadQandA(questionFile, answerFile):
	with open(questionFile, 'r') as file:
		questions = file.read()

	questions = [q for q in questions.split('\n') if q != '']
	with open(answerFile, 'r') as file:
		answers = file.read()
	answers = [a for a in answers.split('\n') if a != '']
	return((np.asarray(questions), np.asarray(answers)))


def ShuffleQandA(questions, answers):
	inds = np.arange(len(questions))
	np.random.shuffle(inds)
	questions = questions[inds]
	answers = answers[inds]
	return ((questions, answers, inds))


def PrettyPrint(order):
	order = order + 1
	number = list(range(1, len(order + 1)))
	for o, n in zip(order, number):
		print(str(n) + ':\t' + str(o))
	return


def PlayTrivia(Qs, As):

	def FlipCard():
		current = cardInfo["text"]
		if current == Qs[0]:
			cardInfo.config(text=As[0])
			flipButton.config(text='Show Question')
		elif current == As[0]:
			cardInfo.config(text=Qs[0])
			flipButton.config(text='Show Answer')

	def NextCard():
		window.destroy()
		PlayTrivia(Qs[1:], As[1:])

	window = tk.Tk()
	window.minsize(1250, 700)

	cardInfo = tk.Label(text=Qs[0], font=("Helvetica", 80), wraplength=1100, justify='left', fg='#1b2b34')
	cardInfo.pack()

	flipButton = tk.Button(text="Show Answer", command=FlipCard)
	flipButton.pack()

	nextButton = tk.Button(text="Go to next question", command=NextCard)
	nextButton.pack()
	window.mainloop()


# Qs = '/Users/matt/Desktop/Trivia/data/questions_short.txt'
# As = '/Users/matt/Desktop/Trivia/data/answers_short.txt'

Qs = '/Users/matt/Desktop/Trivia/data/questions.txt'
As = '/Users/matt/Desktop/Trivia/data/answers_spaced.txt'

questions, answers = ReadQandA(Qs, As)
questions, answers, order = ShuffleQandA(questions, answers)
PrettyPrint(order)


PlayTrivia(questions, answers)

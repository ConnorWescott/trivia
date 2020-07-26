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
	order += 1
	number = list(range(1, len(order) + 1))
	for o, n in zip(order, number):
		print(str(n) + ':\t' + str(o))
	return


def PlayTrivia(Qs, As):

	def FlipCard(event=None):
		current = cardInfo["text"]
		if current == Qs[counter]:
			cardInfo.config(text=As[counter])
			flipButton.config(text='Show Question')
		elif current == As[counter]:
			cardInfo.config(text=Qs[counter])
			flipButton.config(text='Show Answer')

	def NextCard(event=None):
		global counter
		counter += 1
		try:
			cardInfo.config(text=Qs[counter])
			flipButton.config(text='Show Answer')
		except IndexError:
			cardInfo.config(text='No more cards. Thank you for playing :)')
			flipButton.pack_forget()
			nextButton.pack_forget()
			end_btn = tk.Button(master=buttonFrame, text='Click here to exit ', font=("Helvetica Neue", 20), highlightbackground='#1b2b34', fg='#1b2b34', command=window.destroy)
			end_btn.pack()

	window = tk.Tk()
	window.geometry('1200x700')
	window.configure(bg='#1b2b34')

	buttonFrame = tk.Frame(bg='#1b2b34')
	textFrame = tk.Frame(bg='#1b2b34')

	# Setup button to flip card
	flipButton = tk.Button(master=buttonFrame, text="Show Answer", font=("Helvetica Neue", 20), highlightbackground='#1b2b34', fg='#1b2b34', command=FlipCard)
	flipButton.pack(side=tk.LEFT)

	# Setup button to move to next card
	nextButton = tk.Button(master=buttonFrame, text="Go to next question", font=("Helvetica Neue", 20), highlightbackground='#1b2b34', fg='#1b2b34', command=NextCard)
	nextButton.pack(side=tk.LEFT)

	# Setup card info
	cardInfo = tk.Label(master=textFrame, text=Qs[counter], font=("Helvetica Neue", 80), wraplength=1100, justify='left', fg='#cdd3de', bg='#1b2b34')
	cardInfo.pack()

	buttonFrame.pack(side=tk.TOP)
	textFrame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

	# Bind keyboard to arrow keys
	window.bind('<Left>', FlipCard)
	window.bind('<Right>', NextCard)

	window.mainloop()


Qs = '../data/questions_short.txt'
As = '../data/answers_short.txt'

global counter
counter = 0

# Qs = '../data/questions.txt'
# As = '../data/answers_spaced.txt'

questions, answers = ReadQandA(Qs, As)
questions, answers, order = ShuffleQandA(questions, answers)
PrettyPrint(order)


PlayTrivia(questions, answers)
# '#1b2b34'

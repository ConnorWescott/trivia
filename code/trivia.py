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

	questions = np.insert(questions, 0, 'Are You Ready?')
	answers = np.insert(answers, 0, 'Press "Go to next question" to start.')
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
			flipButton.config(text='Show Question (⬅)')
		elif current == As[counter]:
			cardInfo.config(text=Qs[counter])
			flipButton.config(text='Show Answer (⬅)')

	def NextCard(event=None):
		global counter, timer
		counter += 1
		try:
			cardInfo.config(text=Qs[counter], fg=lightGray)
			flipButton.config(text='Show Answer (⬅)')
			timer.destroy()
			timer = tk.Label(master=buttonFrame, text='30', font=("Helvetica Neue Bold", 50), fg=lightGray, bg=darkBlue)
			timer.pack(side=tk.LEFT)
			countdown(30, timer)
		except IndexError:
			timer.destroy()

			cardInfo.config(text='No more cards. Thank you for playing! 🤠')
			flipButton.pack_forget()
			nextButton.pack_forget()
			timer.pack_forget()
			end_btn = tk.Button(master=buttonFrame, text='Click here to exit ', font=("Helvetica Neue Bold", 35), highlightbackground=darkBlue, fg=darkBlue, command=window.destroy)
			end_btn.pack()


	def countdown(seconds, timer):
		timer.config(text=str(seconds))
		if seconds < 1:
			timer.config(fg=lightGray)
			cardInfo.config(fg=lightGray)
			return
		elif seconds <= 5:
			timer.config(fg='red')
			cardInfo.config(fg='red')
			window.after(1000, countdown, seconds - 1, timer)
		elif seconds <= 15:
			timer.config(text=str(seconds), fg=orange)
			cardInfo.config(fg=orange)
			window.after(1000, countdown, seconds - 1, timer)
		elif seconds > 0:
			window.after(1000, countdown, seconds - 1, timer)

	window = tk.Tk()
	window.geometry('1200x700')
	window.configure(bg=darkBlue)

	buttonFrame = tk.Frame(bg=darkBlue)
	textFrame = tk.Frame(bg=darkBlue)

	# Setup button to flip card
	flipButton = tk.Button(master=buttonFrame, text="Show Answer (⬅)", font=("Helvetica Neue Bold", 20), highlightbackground=darkBlue, fg=darkBlue, command=FlipCard)
	flipButton.pack(side=tk.LEFT)

	# Setup button to move to next card
	nextButton = tk.Button(master=buttonFrame, text="(⮕)Go to next question", font=("Helvetica Neue Bold", 20), highlightbackground=darkBlue, fg=darkBlue, command=NextCard)
	nextButton.pack(side=tk.LEFT)

	# Setup the timer label
	global timer
	timer = tk.Label(master=buttonFrame, text='30', font=("Helvetica Neue Bold", 50), fg=lightGray, bg=darkBlue)
	timer.pack(side=tk.LEFT)

	# Setup card info
	cardInfo = tk.Label(master=textFrame, text=Qs[counter], font=("Helvetica Neue", 80), wraplength=1100, justify='left', fg=lightGray, bg=darkBlue)
	cardInfo.pack()

	buttonFrame.pack(side=tk.TOP)
	textFrame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

	# Bind keyboard to arrow keys
	window.bind('<Left>', FlipCard)
	window.bind('<Right>', NextCard)

	window.mainloop()


orange = '#f99157'
darkBlue = '#1b2b34'
lightGray = '#cdd3de'


Qs = '../data/questions_short.txt'
As = '../data/answers_short.txt'

global counter
counter = 0

# Qs = '../data/questions.txt'
# As = '../data/answers_spaced.txt'

np.random.seed(12)
questions, answers = ReadQandA(Qs, As)
questions, answers, order = ShuffleQandA(questions, answers)
PrettyPrint(order)


PlayTrivia(questions, answers)

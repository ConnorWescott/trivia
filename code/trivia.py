# -*- coding: utf-8 -*-
from pathlib import Path

from dataclasses import dataclass, field
import os
import tkinter as tk
import random

global counter
counter = 0

@dataclass
class Topic:
	question: str
	answer: str

@dataclass
class TriviaTopics:
	topic_list: list[Topic] = field(default_factory=list)

	def shuffle(self):
		random.shuffle(self.topic_list)

def ReadQandA(questionFile, answerFile) -> TriviaTopics:
	with open(questionFile, 'r', encoding='utf-8') as file:
		print(questionFile)
		questions = file.read()

	questions = [q for q in questions.split('\n') if q != '']
	with open(answerFile, 'r', encoding='utf-8') as file:
		answers = file.read()
	answers = [a for a in answers.split('\n') if a != '']

	topic_list = list()
	for question, answer in zip(questions, answers):
		topic = Topic(question=question, answer=answer)
		topic_list.append(topic)

	return TriviaTopics(topic_list=topic_list)


def PrettyPrint(trivia_topics: TriviaTopics):
	print('Order of appearance:\tPrinted Question Number')
	for topic in trivia_topics.topic_list:
		print('{}:\t{}'.format(topic.question, topic.answer))
	return


def PrettySave(order, fileHandle):
	# order += 1
	number = list(range(1, len(order) + 1))
	for o, n in zip(order, number):
		line = '{}:\t{}\n'.format(n, o)
		fileHandle.write(line)
	return



def PlayTrivia(trivia_topics: TriviaTopics):

	def FlipCard(event=None):
		current = cardInfo["text"]
		if current == trivia_topics.topic_list[counter].question:
			cardInfo.config(text=trivia_topics.topic_list[counter].answer)
			flipButton.config(text='Show Question (⬅)')
		elif current == trivia_topics.topic_list[counter].answer:
			cardInfo.config(text=trivia_topics.topic_list[counter].question)
			flipButton.config(text='Show Answer (⬅)')

	def NextCard(event=None):
		global counter, timer
		counter += 1
		try:
			cardInfo.config(text=trivia_topics.topic_list[counter].question, fg=lightGray)
			flipButton.config(text='Show Answer (⬅)')
			timer.destroy()
			timer = tk.Label(master=buttonFrame, text='30', font=("Helvetica Neue Bold", 50), fg=lightGray, bg=darkBlue)
			timer.pack(side=tk.LEFT)
			countdown(30, timer)
		except IndexError: # It's not always an IndexError that is the exception 
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
			#cardInfo.config(fg='red')
			window.after(1000, countdown, seconds - 1, timer)
		elif seconds <= 15:
			timer.config(text=str(seconds), fg=orange)
			#cardInfo.config(fg=orange)
			window.after(1000, countdown, seconds - 1, timer)
		elif seconds > 0:
			window.after(1000, countdown, seconds - 1, timer)

	window = tk.Tk()
	window.title("Trivia!")

	w, h = window.winfo_screenwidth(), window.winfo_screenheight()
	window.geometry("%dx%d+0+0" % (w, h))
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
	cardInfo = tk.Label(master=textFrame, text=trivia_topics.topic_list[counter].question, font=("Helvetica Neue", 80), wraplength=1100, justify='left', fg=lightGray, bg=darkBlue)
	cardInfo.pack()

	buttonFrame.pack(side=tk.TOP)
	textFrame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

	# Bind keyboard to arrow keys
	window.bind('<Left>', FlipCard)
	window.bind('<Right>', NextCard)

	window.mainloop()


def GetStartNumber():
	window = tk.Tk()
	window.title("Trivia!")
	window.geometry('1200x700')
	window.configure(bg=darkBlue)
	
	tk.Label(window, text="Question to start on:", font=("Helvetica Neue", 80), fg=lightGray, bg=darkBlue).grid(row=0)
	e1 = tk.Entry(window, font=("Helvetica Neue", 80), fg=darkBlue)
	tk.Button(window, text='Enter', command=window.quit, font=("Helvetica Neue", 80), fg=darkBlue).grid(row=3, column=0, sticky=tk.W, pady=4)
	e1.grid(row=0, column=1)
	window.mainloop()
	number = e1.get()
	window.destroy()
	if number.isdigit():
		return int(number)
	else:
		return 0


orange = '#f99157'
darkBlue = '#1b2b34'
lightGray = '#cdd3de'


Qs = '../data/questionsTest.txt'
As = '../data/answersTest.txt'


if __name__ == '__main__':
	parent_dir = Path(os.getcwd()).parent
	print(parent_dir)
	Qs = parent_dir.as_posix() + r"/data/Questions69.txt"
	As = parent_dir.as_posix() + r"/data/Answers69.txt"

	trivia_topics = ReadQandA(Qs, As)
	trivia_topics.shuffle()
	print(trivia_topics)

	PrettyPrint(trivia_topics)

	# startNumber = GetStartNumber()
	# if startNumber >= len(questions):
	# 	startNumber = 0
	# counter = startNumber

	PlayTrivia(trivia_topics)

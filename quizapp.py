import sqlite3

conn=sqlite3.connect("quiz1.db")
c=conn.cursor()

def add_question():
    c.execute(''' insert into quiz1
                (question,option1,option2,option3,option4,answer)
                values(?,?,?,?,?,?) ''',
    ("What is the capital of India?","New Delhi","Mumbai","Chennai","Kolkata","New Delhi"))
    c.execute(''' insert into quiz1
                (question,option1,option2,option3,option4,answer)
                values(?,?,?,?,?,?) ''',
    ("Who is created python programming language?","Mark Z","Elon Musk","Bill Gates","Guido van Rossum","Guido van Rossum"))
    c.execute(''' insert into quiz1
                (question,option1,option2,option3,option4,answer)
                values(?,?,?,?,?,?) ''',
    ("What was the world's first electronic computer?","UNIVAC","ENIAC","ABC","None of the above","ENIAC"))
    c.execute(''' insert into quiz1
                (question,option1,option2,option3,option4,answer)
                values(?,?,?,?,?,?) ''',
    ("What is the full form of sql?","Structured Query Language","Stylish Question Language","Stylesheet Query Language","Statement Question Language","Structured Query Language"))
    c.execute(''' insert into quiz1
                (question,option1,option2,option3,option4,answer)
                values(?,?,?,?,?,?) ''',
    ("Who is the founder of the www?","Izazul","Charles Babbage","Tim Berners-Lee","Vint Cerf","Tim Berners-Lee"))
    c.execute(''' insert into quiz1
                (question,option1,option2,option3,option4,answer)
                values(?,?,?,?,?,?) ''',
    ("Who is the father of AI?","John McCarthy","Charles Babbage","Alan Turing","Tim Berners-Lee","John McCarthy"))

conn.commit()
print("Questions added successfully")

c.execute('''create table if not exists quiz1
            (id integer primary key autoincrement,
            question text,
            option1 text,
            option2 text,  
            option3 text,
            option4 text,
            answer text)''')

conn.commit()
conn.close()
print("Table created successfully")

import tkinter as tk
import random

class QuizApp:
    def __init__(self,master):
        self.master=master
        self.master.title("Quiz App")
        self.master.geometry("700x500")
        self.master.config(bg="lightblue")
        self.conn=sqlite3.connect('quiz1.db')
        self.cur=self.conn.cursor()
        self.cur.execute("select*from quiz1")
        self.data=self.cur.fetchall()
        random.shuffle(self.data)
        self.qno=0
        self.correct=0
        self.wrong=0
        self.total=len(self.data)
        self.quistion_Lebal=tk.Label(self.master,text=self.data[self.qno][1],font=("Arial",16),bg="lightblue")
        self.quistion_Lebal.pack(pady=20)
        self.var=tk.StringVar()
        self.option1=tk.Radiobutton(self.master,text=self.data[self.qno][2],font=("Arial",14),bg="lightblue",variable=self.var,value=self.data[self.qno][2])
        self.option1.pack(pady=10)
        self.option2=tk.Radiobutton(self.master,text=self.data[self.qno][3],font=("Arial",14),bg="Lightblue",variable=self.var,value=self.data[self.qno][3])
        self.option2.pack(pady=10)
        self.option3=tk.Radiobutton(self.master,text=self.data[self.qno][4],font=("Arial",14),bg="lightblue",variable=self.var,value=self.data[self.qno][4])
        self.option3.pack(pady=10)
        self.option4=tk.Radiobutton(self.master,text=self.data[self.qno][5],font=("Arial",14),bg="lightblue",variable=self.var,value=self.data[self.qno][5])
        self.option4.pack(pady=10)
        self.next_button=tk.Button(self.master,text="Next",font=("Arial",14),bg="brown",command=self.next)
        self.next_button.pack(pady=20)
        self.result_label=tk.Label(self.master,text="",font=("Arial",14),bg="lightblue")
        self.result_label.pack(pady=20)
    def next(self):
        if self.var.get()==self.data[self.qno][6]:
            self.correct+=1
        else:
            self.wrong+=1
        self.qno+=1
        if self.qno==self.total:
            self.quistion_Lebal.config(text="Quiz Completed")
            self.option1.pack_forget()
            self.option2.pack_forget()
            self.option3.pack_forget()
            self.option4.pack_forget()
            self.next_button.pack_forget()
            self.result_label.config(text=f"Correct: {self.correct}\nWrong: {self.wrong}\nTotal: {self.total}")
        else:
            self.quistion_Lebal.config(text=self.data[self.qno][1])
            self.option1.config(text=self.data[self.qno][2],value=self.data[self.qno][2])
            self.option2.config(text=self.data[self.qno][3],value=self.data[self.qno][3])
            self.option3.config(text=self.data[self.qno][4],value=self.data[self.qno][4])
            self.option4.config(text=self.data[self.qno][5],value=self.data[self.qno][5])
            self.var.set("")
            self.result_label.config(text="")
if __name__=="__main__":
    root=tk.Tk()
    app=QuizApp(root)
    root.mainloop()

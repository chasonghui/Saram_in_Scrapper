from flask import Flask, render_template,request,redirect,send_file
from scrapper import get_jobs
from exporter import save_to_file
app=Flask("Scrapper")

db={}#fake DB

@app.route("/")
def home():
  return render_template("potato.html")

@app.route("/report")
def report():
  word=request.args.get('word')#arg : /report?args=1&args3=2이런식으로 전달되는것
  if word:
    word = word.lower()
    existingJobs = db.get(word)#검색한 word가 db에 있는지 찾아봄
    if existingJobs:
     jobs=existingJobs
    else:
      jobs=get_jobs(word)#scrapping 동작
      db[word]=jobs#scrapping하고 db['word']에 저장됨
  else: #word가 존재하지 않을 경우 home으로 redirect
    return redirect("/")
  #render_templeate함수를 리턴하면서, report.html을 렌더링
  return render_template("report.html",
    searchingBy=word,

    resultsNumber=len(jobs),#fakeDB에서 긁어온 jobs의 개수
    jobs=jobs#report.html에 jobs넘겨주기
  )

@app.route("/export")
def export():
  try:
    word=request.args.get('word')
    if not word:
      raise Exception()
    word=word.lower()
    jobs=db.get(word)
    if not jobs:
      raise Exception()
    save_to_file(jobs)
    return send_file("jobs.csv")
  except:
    return redirect("/")

app.run(host="0.0.0.0")


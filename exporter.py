import csv

def save_to_file(jobs):
  file=open("jobs.csv",mode="w")#파일 열기, 파일변수에 저장
  writer = csv.writer(file)#wirter만들기
  writer.writerow(["title","company","location","link"])
  for job in jobs:
    writer.writerow(list(job.values()))
  return
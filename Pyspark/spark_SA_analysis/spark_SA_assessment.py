from textblob import TextBlob
from pyspark import SparkConf, SparkContext
import re

def abb_en(line):
   abbreviation_en = {
    'u': 'you',
    'thr': 'there',
    'asap': 'as soon as possible',
    'lv' : 'love',    
    'c' : 'see'
   }
   
   abbrev = ' '.join (abbreviation_en.get(word, word) for word in line.split())
   return (abbrev)

def remove_features(data_str):
   
    url_re = re.compile(r'https?://(www.)?\w+\.\w+(/\w+)*/?')    
    mention_re = re.compile(r'@|#(\w+)')  
    RT_re = re.compile(r'RT(\s+)')
    num_re = re.compile(r'(\d+)')
    
    data_str = str(data_str)
    data_str = RT_re.sub(' ', data_str)  
    data_str = data_str.lower()  
    data_str = url_re.sub(' ', data_str)   
    data_str = mention_re.sub(' ', data_str)  
    data_str = num_re.sub(' ', data_str)
    return data_str

#Write your main function here
def main(sc,filename):
   
   rawdata=sc.textFile(filename).map(lambda x:x.split(',')).filter(lambda x:len(x)==10).filter(lambda x:len(x[0])>1)
    
   tweets = rawdata.map(lambda x:x[1]).map(lambda x:x.lower()).map(lambda x:remove_features(x)).map(lambda x:abb_en(x))\
            .map(lambda x:'Positive' if (TextBlob(x).sentiment.polarity)>0 else 'Negative' if (TextBlob(x).sentiment.polarity)<0 else 'Neutral')

   newdata = rawdata.zip(tweets).map(lambda x:str(x).replace("'",'').replace('"',''))

   newdata.saveAsTextFile('mockexam')
   print('Alhamdulillah')
   print(newdata.take(2))
   
if __name__ == "__main__":

   # Configure your Spark environment
   conf = SparkConf().setMaster("local[1]").setAppName("DE22C03")
   sc = SparkContext(conf=conf)
   # CODE IT YOURSELF
  
   filename = "bitcoin.csv"
  
   main(sc,filename)

   sc.stop()

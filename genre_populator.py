from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Genre, Base, Songs, User

engine = create_engine('sqlite:///musicgenreswithusers.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# User
User1 = User(name = "Tommy Trojan", email = "TinyTom@trojanmail.com",
	picture = "https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png")

session.add(User1)
session.commit()

# Genres
genre1 = Genre(name="Hip-Hop", user = User1)

session.add(genre1)
session.commit()

genre2 = Genre(name="Country", user = User1)

session.add(genre2)
session.commit()

genre3 = Genre(name="Pop", user = User1)

session.add(genre3)
session.commit()

genre4 = Genre(name="Jazz", user = User1)

session.add(genre4)
session.commit()

genre5 = Genre(name="EDM", user = User1)

session.add(genre5)
session.commit()

# Songs

song1 = Songs(name="Country Grammar (Hot in Here)", album="Country Grammar", artist="Nelly", year=2000, length = "3:47", genre=genre1, user = User1)

session.add(song1)
session.commit()

song2 = Songs(name="Black Beattles", album="SremmLife 2", artist="Rae Sremmurd", year=2016, length = "4:52", genre=genre1, user = User1)

session.add(song2)
session.commit()

song3 = Songs(name="Push It", album="Hot, Cool & Viscious", artist="Salt-N-Pepa", year=1986, length = "4:33", genre=genre1, user = User1)

session.add(song3)
session.commit()

song4 = Songs(name="Fight the Power", album="Fear of a Black Planet", artist="Public Enemy", year=1990, length = "5:20", genre=genre1, user = User1)

session.add(song4)
session.commit()

song5 = Songs(name="Rap God", album="The Marshall Mathers LP 2", artist="Eminem", year=2013, length = "6:09", genre=genre1, user = User1)

session.add(song5)
session.commit()

song6 = Songs(name="Die a Happy Man", album="Tangled Up", artist="Thomas Rhett", year=2015, length = "4:03", genre=genre2, user = User1)

session.add(song6)
session.commit()

song7 = Songs(name="Forever And Ever, Amen", album="Always & Forever", artist="Randy Travis", year=1987, length = "4:23", genre=genre2, user = User1)

session.add(song7)
session.commit()

song8 = Songs(name="Achy Breaky Heart", album="Some Gave All", artist="Billy Ray Cyrus", year=1992, length = "3:54", genre=genre2, user = User1)

session.add(song8)
session.commit()

song9 = Songs(name="Think of You", album="I'm Comin' Over", artist="Chris Young", year=2015, length = "3:40", genre=genre2, user = User1)

session.add(song9)
session.commit()

song10 = Songs(name="John Cougar, John Deere, John 3:16", album="Ripcord", artist="Keith Urban", year=2016, length = "3:51", genre=genre2, user = User1)

session.add(song10)
session.commit()

song11 = Songs(name="Uptown Funk ft. Bruno Mars", album="Uptown Funk", artist="Mark Ronson", year=2014, length = "4:30", genre=genre3, user = User1)

session.add(song11)
session.commit()

song12 = Songs(name="What Do You Mean?", album="Purpose", artist="Justin Bieber", year=2015, length = "4:57", genre=genre3, user = User1)

session.add(song12)
session.commit()

song13 = Songs(name="We Found Love", album="Talk That Talk", artist="Calvin Harris", year=2011, length = "5:53", genre=genre3, user = User1)

session.add(song13)
session.commit()

song14 = Songs(name="Shake It Off", album="1989", artist="Taylor Swift", year=2014, length = "4:02", genre=genre3, user = User1)

session.add(song14)
session.commit()

song15 = Songs(name="We Can't Stop", album="Bangerz", artist="Miley Cyrus", year=2013, length = "3:33", genre=genre3, user = User1)

session.add(song15)
session.commit()

song16 = Songs(name="Mack the Knife", album="That's All", artist="Bobby Darin", year=1959, length = "3:13", genre=genre4, user = User1)

session.add(song16)
session.commit()

song17 = Songs(name="Georgia On My Mind", album="Ray, Rare and Live", artist="Ray Charles", year=2003, length = "3:57", genre=genre4, user = User1)

session.add(song17)
session.commit()

song18 = Songs(name="It's Only a Paper Moon", album="Luck So and So", artist="Ella Fitzgerald", year=1951, length = "2:40", genre=genre4, user = User1)

session.add(song18)
session.commit()

song19 = Songs(name="Don't Know Why", album="Come Away With Me", artist="Norah Jones", year=2002, length = "3:11", genre=genre4, user = User1)

session.add(song19)
session.commit()

song20 = Songs(name="Forever In Love", album="Breathless", artist="Kenny G", year=1992, length = "4:07", genre=genre4, user = User1)

session.add(song20)
session.commit()

song21 = Songs(name="This is What You Came For ft. Rihanna", artist="Calvin Harris", year=2016, length = "3:59", genre=genre5, user = User1)

session.add(song21)
session.commit()

song22 = Songs(name="Never Be Like You ft. Kai", album = "Skin", artist="Flume", year=2016, length = "3:53", genre=genre5, user = User1)

session.add(song22)
session.commit()

song23 = Songs(name="Scary Monsters and Nice Sprites", album = "Scary Monsters and Nice Sprites", artist="SKRILLEX", year=2010, length = "4:05", genre=genre5, user = User1)

session.add(song23)
session.commit()

song24 = Songs(name="You're Gonna Love Again", album = "Collateral", artist="Nervo", year=2012, length = "3:44", genre=genre5, user = User1)

session.add(song24)
session.commit()

song25 = Songs(name="I Am Strong ft. Priscilla Ahn", album = "Kaleidoscope", artist="Tiesto", year=2009, length = "3:24", genre=genre5, user = User1)

session.add(song25)
session.commit()


print "added songs!"
from app import db, Movie
from app import app

with app.app_context():
    db.create_all()

    film1 = Movie(title='Mickey 17', cinema='Multiplex', price=180.0, image='Mickey17Film.png')
    film2 = Movie(title='It', cinema='Planeta Kino', price=200.0, image='ItFilm.jpg')
    film3 = Movie(title='Oppenheimer', cinema='Multiplex', price=170.0, image='OpenheimerFilm.jpg')
    film4 = Movie(title='Minecraft Movie', cinema='Cinema City', price=100.0, image='minecraftFilm.jpg')
    film5 = Movie(title='Star Wars EP III', cinema='Multiplex', price=150.0, image='StarWarsEP3.jpg')
    film6 = Movie(title='Until Dawn', cinema='Planeta Kino', price=190.0, image='UntilDawnFilm.jpeg')
    film7 = Movie(title='The Green Mile', cinema='Cinema City', price=125.0,image='GreenMileFilm.jpg')
    film8 = Movie(title='The Da Vinci Code', cinema='Multiplex', price=150.0, image='TheDaVinciCodeFilm.jpg')

    db.session.add_all([film1, film2, film3, film4, film5, film6, film7, film8])
    db.session.commit()

    print("Фільми додано успішно")

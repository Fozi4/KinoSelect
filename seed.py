from app import db, Movie
from app import app

with app.app_context():
    db.create_all()

    film1 = Movie(
        title='Mickey 17',
        cinema='Multiplex',
        price=180.0,
        image='Mickey17Film.png',
        description='A disposable employee on a dangerous mission to colonize an ice world repeatedly regenerates after death.'
    )

    film2 = Movie(
        title='It',
        cinema='Planeta Kino',
        price=200.0,
        image='ItFilm.jpg',
        description='A group of kids faces their worst nightmare — a shape-shifting clown that feeds on their fears.'
    )

    film3 = Movie(
        title='Oppenheimer',
        cinema='Multiplex',
        price=170.0,
        image='OpenheimerFilm.jpg',
        description='A gripping biopic about J. Robert Oppenheimer and the moral dilemmas behind the atomic bomb.'
    )

    film4 = Movie(
        title='Minecraft Movie',
        cinema='Cinema City',
        price=100.0,
        image='minecraftFilm.jpg',
        description='An adventure-filled journey in the pixelated world of Minecraft, filled with creativity and peril.'
    )

    film5 = Movie(
        title='Star Wars EP III',
        cinema='Multiplex',
        price=150.0,
        image='StarWarsEP3.jpg',
        description='Anakin Skywalker falls to the dark side as the Galactic Republic begins to collapse.'
    )

    film6 = Movie(
        title='Until Dawn',
        cinema='Planeta Kino',
        price=190.0,
        image='UntilDawnFilm.jpeg',
        description='A group of friends fights to survive a night in the mountains where horrors from the past return.'
    )

    film7 = Movie(
        title='The Green Mile',
        cinema='Cinema City',
        price=125.0,
        image='GreenMileFilm.jpg',
        description='A prison guard discovers a death row inmate with miraculous healing powers.'
    )

    film8 = Movie(
        title='The Da Vinci Code',
        cinema='Multiplex',
        price=150.0,
        image='TheDaVinciCodeFilm.jpg',
        description='A symbologist uncovers a secret that could shake the foundations of Christianity.'
    )

    film9 = Movie(
        title='Interstellar',
        cinema='Planeta Kino',
        price=210.0,
        image='InterstellarFilm.jpg',
        description='A team of astronauts travels through a wormhole to find a new home for humanity.'
    )

    film10 = Movie(
        title='Joker',
        cinema='Cinema City',
        price=195.0,
        image='JokerFilm.jpg',
        description='A mentally troubled comedian descends into madness and becomes Gotham’s infamous villain.'
    )

    film11 = Movie(
        title='Inception',
        cinema='Multiplex',
        price=185.0,
        image='InceptionFilm.jpg',
        description='A skilled thief enters people’s dreams to steal secrets — or plant new ideas.'
    )

    film12 = Movie(
        title='Dune: Part Two',
        cinema='Multiplex',
        price=220.0,
        image='DunePart2Film.jpeg',
        description='Paul Atreides rises as a leader to fulfill his destiny and unite the desert planet.'
    )

    film13 = Movie(
        title='Barbie',
        cinema='Cinema City',
        price=160.0,
        image='BarbieFilm.jpg',
        description='Barbie steps into the real world on a self-discovery journey like never before.'
    )

    film14 = Movie(
        title='The Batman',
        cinema='Planeta Kino',
        price=200.0,
        image='TheBatmanFilm.png',
        description='Batman investigates a series of murders linked to corruption in Gotham City.'
    )

    film15 = Movie(
        title='Avengers: Endgame',
        cinema='Multiplex',
        price=230.0,
        image='AvengersEndgameFilm.jpg',
        description='The Avengers regroup for one final mission to undo the destruction caused by Thanos.'
    )

    film16 = Movie(
        title='Shutter Island',
        cinema='Cinema City',
        price=170.0,
        image='ShutterIslandFilm.webp',
        description='A U.S. Marshal uncovers dark secrets during an investigation at a remote asylum.'
    )
    db.session.add_all([film1, film2, film3, film4, film5, film6, film7, film8, film9, film10, film11, film12,
                       film13, film14, film15, film16])

    db.session.commit()
    print("Фільми додано успішно")

from flask import Flask, jsonify, render_template, request, abort
import sqlite3

app = Flask(__name__, static_url_path='/static')

news_items = [
    {
        "slug": "stipendiya-prezidenta-ukraini",
        "title": "Стипендія Президента України",
        "description": "270 талановитих українських школярів, що є переможцями Всеукраїнського конкурсу-захисту МАН та IV етапу всеукраїнських учнівських олімпіад, отримали стипендії.",
        "button_text": "Дивитись більше",
        "image": "/static/images/news1.jpg",
        "image_secondary": "/static/images/news9.jpg",
        "content": """
            11 грудня 270 талановитих українських школярів, що є переможцями III етапу Всеукраїнського конкурсу-захисту МАН та IV етапу всеукраїнських учнівських олімпіад, отримали стипендії Президента України. Урочистості з нагоди нагородження стипендіатів відбулися в залі засідань Вченої ради Національного технічного університету України «КПІ імені Ігоря Сікорського». Привітати й нагородити лауреатів завітали міністр освіти і науки України Оксен Лісовий, президент Малої академії наук Станіслав Довгий, президент Національної академії наук України Анатолій Загородній, директор Інституту модернізації змісту освіти Євген Баженков та інші поважні гості. Приємно відмітити, що серед цьогорічних лауреатів є і учениця нашого ліцею, одинадцятикласниця Марія Христиченко. Вітаємо Марію з почесним званням стипендіатки Президента України!
        """
    },
    {
        "slug": "den-zahisnikiv-i-zahisnits",
        "title": "День Захисників і Захисниць України",
        "description": "1 жовтня ми вітаємо тих героїв, які ціною власного життя боронять Україну, бережуть спокій і дарують надію на наше вільне і щасливе майбутнє",
        "button_text": "Дивитись більше",
        "image": "/static/images/news12.jpg",
        "image_secondary": "/static/images/news15.jpg",
        "content": """Вклоняємось доземно українському воїну! День Захисників і Захисниць України набув особливого значення для нашої країни. 1 жовтня ми вітаємо тих героїв, які ціною власного життя боронять Україну, бережуть спокій і дарують надію на наше вільне і щасливе майбутнє. Від щирого серця, з любов’ю і великою пошаною дякуємо кожному і кожній, хто мужньо захищає нашу державу! З нагоди цього дня в нашому закладі освіти відбулися різноманітні тематичні заходи. Підтримуємо ЗСУ! Разом до ПЕРЕМОГИ!
        """
    },
    {
        "slug": "peremoznichia-olimpiadi-geogr",
        "title": "Переможниця Всеукраїнської учнівської олімпіади з географії",
        "description": "Вітаємо Христиченко Марію, ученицю 11-А класу, переможницю IV (четвертого) етапу",
        "button_text": "Дивитись більше",
        "image": "/static/images/news3.jpg",
        "image_secondary": "/static/images/news16.jpg",
        "content": """Вітаємо Христиченко Марію, ученицю 11-А класу, переможницю IV (четвертого) етапу Всеукраїнської учнівської олімпіади з географії (вчителька географії Г.І.Шумейко) - Диплом ІІІ ступеня. Олімпіада тривала у місті Луцьку з 01 по 05 квітня 2024 року. Пишаємось вашими успіхами! Бажаємо міцного здоров’я, добробуту та щастя, не зупинятися на досягнутому, а рухатись «через терни до зірок»!
        """
    },
    {
        "slug": "den-vchitelya",
        "title": "День вчителя",
        "description": "Наші креативні учні продовжують нас дивувати!",
        "button_text": "Дивитись більше",
        "image": "/static/images/news11.jpg",
        "image_secondary": "/static/images/news17.jpg",
        "content": """Наші 💙💛креативні учні продовжують нас 😍дивувати! Вони дотепні, творчі, дружні і при цьому дуже індивідуальні. Джерелом нашого натхнення є саме вони!
        """
    },
    {
        "slug": "vipusk-2024",
        "title": "Випуск 2024",
        "description": "Молоді, перспективні, здатні втілити мрії в реальність люди - це наші випускники, це наш сьогоднішній день і наше майбутнє.",
        "button_text": "Дивитись більше",
        "image": "/static/images/news13.jpg",
        "image_secondary": "/static/images/news18.jpg",
        "content": """Наші 🧑‍🎓👩‍🎓випускники – наша гордість і надія! Молоді, перспективні, здатні втілити мрії в реальність люди - це наші випускники, це наш сьогоднішній день і наше майбутнє. Зичимо вам, наші дорогі, мирного неба над головою, впевненості у своїх силах. Нехай ваша подорож у майбутнє буде наповнена радістю, успіхом і виконанням всіх ваших мрій. Тож у добру путь!
        """
    },
    {
        "slug": "stop-booling",
        "title": "Міжнародний день боротьби з насильством і булінгом",
        "description": "Завдання кожного з нас — виховувати культуру поваги, підтримки й емпатії.",
        "button_text": "Дивитись більше",
        "image": "/static/images/news14.jpg",
        "image_secondary": "/static/images/news19.jpg",
        "content": """7 листопада – Міжнародний день боротьби з насильством і булінгом у закладах освіти. Завдання кожного з нас — виховувати культуру поваги, підтримки й емпатії. Саме тому, в нашому ліцеї відбулись тематичні заходи, зокрема практичний психолог Нелеп О.О. та соціальний педагог Тиченок О.О. провели інформаційно-просвітницькі бесіди з елементами тренінгу «Стоп булінг» для учнів 7-х класів. Мета проведення заходів полягала в ознайомленні учнів з поняттям, формами, структурою булінгу та його наслідками, а також запобіганні і протидії психологічному, фізичному або емоційному насильству. В ході проведення заходів підлітки отримали практичні поради про те, як діяти, якщо опинилися в ситуації булінгу. Також розвинули навички протидії соціальному тиску, вміння пошуку шляхів виходу зі складної ситуації та формували навики відповідальної та безпечної поведінки. Зараз українське суспільство переживає складні часи, тому ми як ніколи маємо бути згуртованими і чуйними у вирішенні багатьох питань, особливо тих, що стосуються розвитку і безпеки підростаючого покоління. Будуймо разом світ, у якому пануватимуть розуміння, взаємоповага та турбота!
        """
    },
]

teacher_profile = [
    {
        "name": "Дарина Сергіївна",
        "image": "static/images/teacher1.jpg",
        "alt_text": "Дарина Сергіївна",
        "bio": """Я — вчителька математики.
         Моя головна мета — допомогти дітям не просто вивчати формули, а дійсно зрозуміти математику. У своїй роботі я використовую різноманітні підходи, щоб кожен учень міг знайти щось цікаве для себе та впевнено просуватися у вивченні предмету. Вірю, що математика може бути доступною і захопливою, і прагну розвивати у своїх учнів не лише знання, а й критичне та логічне мислення. 
         Буду рада допомогти кожному, хто хоче зробити крок у світ чисел та розрахунків!"""

    },
    {
        "name": "Анастасія Андріївна",
        "image": "static/images/teacher2.jpg",
        "alt_text": "Анастасія Андріївна",
        "bio": """Я — вчителька української мови. 
        Моя мета — допомогти учням не лише опанувати правила, а й по-справжньому полюбити рідну мову. На уроках я стараюся створити дружню атмосферу, щоб кожен відчував себе комфортно і впевнено. Використовую різні методи, щоб зробити навчання цікавим, сучасним і захопливим.
        Вірю, що знання мови відкриває нові горизонти і допомагає розвивати особистість, тому радо підтримую своїх учнів на цьому шляху"""
    },
    {
        "name": "Вікторія Анатоліївна",
        "image": "static/images/teacher3.jpg",
        "alt_text": "Вікторія Анатоліївна",
        "bio": """Я — вчителька інформатики. 
        Моя мета — показати учням, що інформатика — це не лише комп’ютери та програми, а цілий світ можливостей та креативності. На своїх уроках я поєдную теорію з практичними завданнями, щоб кожен міг набути необхідних навичок для сучасного цифрового світу.
         Від основ програмування до безпеки в Інтернеті — прагну, щоб кожен учень відкрив для себе щось нове і корисне. Рада підтримати вас на шляху до технологічних знань!"""
    },
    {
        "name": "Карина В'ячеславівна",
        "image": "static/images/teacher4.jpg",
        "alt_text": "Карина В'ячеславівна",
        "bio": """Я — вчителька англійської мови.
         Моя мета — показати учням, що англійська — це не лише мова, а й ключ до нового світу можливостей, спілкування та культури. На своїх уроках я поєдную граматику з практичними завданнями, щоб кожен зміг не тільки вивчити мову, а й вільно використовувати її в реальному житті. 
         Від основ комунікації до вивчення літератури та культури англомовних країн — прагну, щоб кожен учень відкрив для себе щось нове та корисне. Рада підтримати вас на шляху до знань і впевненості в спілкуванні англійською!"""
    },
    {
        "name": "Григорій Миколайович",
        "image": "static/images/teacher5.jpg",
        "alt_text": "Григорій Миколайович",
        "bio": """Я — вчитель фізичної культури. 
        Моя мета — показати учням, що фізична культура — це не тільки спорт, а й здоров’я, енергія та гармонія тіла і духу. На своїх уроках я поєдную рухливі ігри з фізичними вправами, щоб кожен міг знайти свою улюблену активність і покращити фізичну форму. 
        Від основ здорового способу життя до командних видів спорту — прагну, щоб кожен учень зрозумів важливість активного відпочинку та навчився працювати в команді. Радий підтримати вас на шляху до здоров’я та фізичної витривалості!"""
    },
    {
        "name": "Андрій Олексійович",
        "image": "static/images/teacher6.jpg",
        "alt_text": "Андрій Олексійович",
        "bio": """Я — вчитель фізики. 
        Моя мета — показати учням, що фізика — це не лише складні формули та досліди, а цілий світ закономірностей, які пояснюють, як влаштована наша реальність. На своїх уроках я поєдную теорію з практичними експериментами, щоб кожен міг зрозуміти, як фізичні закони впливають на повсякденне життя.
        Від механіки до електромагнетизму — прагну, щоб кожен учень розумів, як фізика допомагає пояснити явища навколо нас. Рада підтримати вас у відкритті світу науки та технологій!"""
    }
]

winners = [
    {
        "name": "Андрій Шевченко",
        "description": "Переможець IV етапу Всеукраїнської олімпіади з біології",
        "image": "static/images/boy4.jpg"
    },
    {
        "name": "Катерина Сидоренко",
        "description": "Переможниця II етапу Всеукраїнської олімпіади з історії",
        "image": "static/images/girl3.jpg"
    },
    {
        "name": "Сергій Кравчук",
        "description": "Переможець II етапу Всеукраїнського конкурсу-захисту МАН",
        "image": "static/images/boy5.jpg"
    },
    {
        "name": "Олена Петренко",
        "description": "Переможниця III етапу Всеукраїнської олімпіади з математики",
        "image": "static/images/girl2.jpg"
    },
    {
        "name": "Марія Ткаченко",
        "description": "Переможниця I етапу Всеукраїнської олімпіади з хімії",
        "image": "static/images/girl1.jpg"
    },
    {
        "name": "Григорій Лук'яненко",
        "description": "Переможець III етапу Всеукраїнської олімпіади з мистецтва",
        "image": "static/images/boy6.jpg"
    }
]

events_list = [
    {
        "title": "Прикрасимо ялинку",
        "image": "static/images/christmasstree.jpg",
        "alt_text": "Прикрасимо ялинку",
        "description": """5 грудня в холі школи відбудеться прикрашання ялинки, де учні разом з вчителями створять святкову атмосферу. Це буде чудова можливість для всіх долучитися до зимових традицій та підготуватися до новорічних свят.""",
    },
    {
        "title": "Літературний конкурс",
        "image": "static/images/books.jpg",
        "alt_text": "Літературний конкурс",
        "description": """Запрошуємо учнів до участі в літературному конкурсі, де кожен може поділитися своєю творчістю. Учасники можуть написати вірші, есе чи оповідання на задану тему. Найкращі твори будуть опубліковані в шкільному журналі.
        Прийди та поділись своїм талантом!""",
    },
    {
        "title": "Квест з інформатики",
        "image": "static/images/inform.jpg",
        "alt_text": "Квест з інформатики",
        "description": """Запрошуємо всіх учнів на захоплюючий квест з інформатики! Вам потрібно буде розв’язувати задачі, пов'язані з програмуванням, алгоритмами та логікою, щоб знайти захований скарб. Це чудова можливість не тільки перевірити свої навички, а й весело провести час.
        Регистрируйся та бери участь у квесті!""",
    },
    {
        "title": "Футбольний матч",
        "image": "static/images/sport.jpg",
        "alt_text": "Футбольний матч",
        "description": """18 грудня відбудеться захоплюючий футбольний матч, у якому учні змагатимуться за першість. Це буде чудова можливість підтримати команду та насолодитися спортивною атмосферою перед зимовими канікулами.""",
    },
    {
        "title": "16 днів проти насильства",
        "image": "static/images/bullying.jpg",
        "alt_text": "16 днів проти насильства",
        "description": """25.11 стартує щорічна всеукраїнська акція "16 днів проти насильства" """,
    },
]


def get_photos():
    conn = sqlite3.connect("gallery.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, image_url, likes FROM photos")
    photos = [
        {"id": row[0], "image_url": row[1], "likes": row[2]} for row in cursor.fetchall()
    ]
    conn.close()
    return photos


def update_likes(photo_id):
    conn = sqlite3.connect("gallery.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE photos SET likes = likes + 1 WHERE id = ?", (photo_id,))
    conn.commit()
    cursor.execute("SELECT likes FROM photos WHERE id = ?", (photo_id,))
    updated_likes = cursor.fetchone()[0]
    conn.close()
    return updated_likes


@app.route('/')
def index():
    return render_template('index.html', news_items=news_items, events_list=events_list)


@app.route("/gallery")
def gallery():
    photos = get_photos()
    return render_template("photogalery.html", photos=photos)


@app.route("/like/<int:photo_id>", methods=["POST"])
def like_photo(photo_id):
    try:
        updated_likes = update_likes(photo_id)
        return jsonify({"success": True, "likes": updated_likes})
    except:
        return jsonify({"success": False}), 404


@app.route('/news')
def news():
    return render_template('news.html', news_items=news_items)


@app.route('/test')
def test():
    return render_template('test.html')


@app.route('/contacts')
def contacts():
    return render_template('contacts.html')


@app.route('/news/<slug>')
def news_detail(slug):
    # Find the specific news item by slug
    news_item = next((item for item in news_items if item['slug'] == slug), None)

    if news_item:
        return render_template('itnews.html', news_item=news_item)
    else:
        return "News not found", 404


@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html', winners=winners)


@app.route("/teachers")
def teachers():
    # Use the teacher_profile directly
    page = request.args.get('page', 1, type=int)
    teachers_per_page = 3
    start = (page - 1) * teachers_per_page
    end = start + teachers_per_page
    teachers_to_display = teacher_profile[start:end]
    total_pages = (len(teacher_profile) + teachers_per_page - 1) // teachers_per_page

    if page < 1 or page > total_pages:
        abort(404)

    return render_template(
        "teachers.html",
        teachers=teachers_to_display,
        current_page=page,
        total_pages=total_pages
    )


if __name__ == '__main__':
    app.run(port=8080, debug=True)

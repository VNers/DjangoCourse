from django.core.management.base import BaseCommand
from sungrilla.models import Category, Product
from django.utils import timezone


class Command(BaseCommand):
    help = 'Populates the database with initial data.'

    def handle(self, *args, **kwargs):
        products_data = {
            "POOL RELAX": [
                {"name": "ШЕЗЛОНГ БУДНІ", "image": "product_images/shezlong.png", "portion_size": "1 персона", "price": 500.00},
                {"name": "ШЕЗЛОНГ ВИХІДНІ", "portion_size": "1 персона", "price": 700.00},
                {"name": "ЛІЖКО БУДНІ", "portion_size": "2-4 персони", "price": 1200.00},
                {"name": "ЛІЖКО ВИХІДНІ", "portion_size": "2-4 персони", "price": 1700.00},
                {"name": "БУНГАЛО БУДНІ", "portion_size": "4-8 персони", "price": 2000.00},
                {"name": "БУНГАЛО ВИХІДНІ", "portion_size": "4-8 персони", "price": 2500.00},
            ],
            "STARTERS": [
                {"name": "БРУСКЕТИ З ПРОШУТО", "portion_size": "110 г", "price": 245.00},
                {"name": "БРУСКЕТИ 3 ПOCOCEM", "portion_size": "130 г", "price": 245.00},
                {"name": "ГУАКАМОПЕ 3 НАЧОС", "portion_size": "150/30 г", "price": 220.00},
                {"name": "КАРПАЧО 3 ТЕПЯТИНИ", "portion_size": "220 г", "price": 290.00},
                {"name": "СИРИ ITAЛІЇ", "portion_size": "190/50 г", "price": 390.00},
                {"name": "СЕТ ІТАf1ІЙСЬКИХ ДЕПІКАТЕСІВ", "portion_size": "560 г", "price": 450.00},
                {"name": "КУКУРУДЗА ГРИПЬ", "portion_size": "300/50 г", "price": 180.00},
                {"name": "КУРЯЧІ КРИЛЬЦЯ ВВQ", "portion_size": "240/50/50 г", "price": 240.00},
                {"name": "СИРНИЙ ПАВАШ НА ГРИПІ", "portion_size": "200 г", "price": 210.00},
                {"name": "СИРНИЙ ПАВАШ 3 ТЕПЯТИНОЮ НА ГРИПІ", "portion_size": "240 г", "price": 280.00},
                {"name": "КАМАМБЕР ФРІ 3 ЖУРАВПИННИМ СОУСОМ", "portion_size": "200/50 г", "price": 250.00},
                {"name": "ТИГРОВІ КРЕВЕТКИ НА ПОДУШЦІ 3 ГУАКАМОПЕ", "portion_size": "175 г", "price": 390.00},
            ],
            "SALADS": [
                {"name": "ГРЕЦЬКИЙ CAПAT 3 СИРОМ ФЕТА", "portion_size": "290 г", "price": 250},
                {"name": "CAПAT 3 ТЕППИМ КАМАМБЕРОМ ТА MIKCOM CAПATУ", "portion_size": "190 г", "price": 250},
                {"name": "ЦЕЗАР 3 ІНДИЧКОЮ ГРИПЬ", "portion_size": "250 г", "price": 290},
                {"name": "CAПAT 3 ПOCOCEM", "portion_size": "180 г", "price": 350},
            ],
            "GRILL": [
                {"name": "ШАШПИК 3 ФІПЕ ІНДИЧКИ", "portion_size": "100/50/40/60 г", "price": 190},
                {"name": "ШАШПИК 3 ЯЛОВИЧИНИ", "portion_size": "100/40/30/ г", "price": 250},
                {"name": "СТЕЙК 3 ЛОСОСЯ", "portion_size": "150/40 г", "price": 390},
            ],
            "BURGERS": [
                {"name": "БУРГЕР 3 ІНДИЧКОЮ", "portion_size": "280/100/30/30 г", "price": 390},
                {"name": "БУРГЕР 3 ТЕЛЯТИНОЮ", "portion_size": "320/100/30/30 г", "price": 390},
            ],
            "PASTA": [
                {"name": "KAPBOHAPA", "portion_size": "270 г", "price": 290},
                {"name": "ІТАЛІЙСЬКИЙ СІФУД: "
                         "ТАЛЬЯТЕЛЛЕ 3 ПOCOCEM ТА КРЕВЕТКОЮ", "portion_size": "340 г", "price": 350},
            ],
            "MAIN DISHES": [
                {"name": "СТЕЙК ІНДИЧКИ 3 OВОЧЕВОЮ CAЛЬСОЮ", "portion_size": "230 г", "price": 390},
                {"name": "ФІЛЕ MІHЬЙOH 3І СПАРЖЕЮ ACПAPAГУС", "portion_size": "250 г", "price": 490},
                {"name": "ЛОКШИНА WOG З ТЕЛЯТИНОЮ ТА ОВОЧАМИ", "portion_size": "350 г", "price": 290},
            ],
            "SOUPS": [
                {"name": "КУРЯЧИЙ БУЛЬЙОН", "portion_size": "250 г", "price": 180},
                {"name": "ОКРОШКА НА АЙРАНІ", "portion_size": "270 г", "price": 180},
                {"name": "ГАСПАЧО", "portion_size": "260 г", "price": 180},
            ],
            "SIDE DISHED": [
                {"name": "КАРТОПЛЯ ФРІ", "portion_size": "150 г", "price": 120},
                {"name": "БАТАТ ФРІ", "portion_size": "150 г", "price": 120},
                {"name": "ОВОЧІ ГРИЛЬ", "portion_size": "280 г", "price": 250},
            ],
            "DESSERTS": [
                {"name": "МОРОЗИВО", "portion_size": "50 г", "price": 100},
                {"name": "ЧИЗКЕЙК З ПОЛУНИЧНИМ СОУСОМ", "portion_size": "150/50/30 г", "price": 190},
                {"name": "ФРУКТОВЕ ПЛАТО", "portion_size": "480 г", "price": 350},
            ],
            "MODERN COCKTAILS": [
                {"name": "SUNSET-SPRITZ", "portion_size": "250 мл", "price": 299},
                {"name": "BOTANICAL GARDEN", "portion_size": "250 мл", "price": 275},
                {"name": "ARUBA", "portion_size": "250 мл", "price": 275},
                {"name": "SEVILA FLAVOR", "portion_size": "200 мл", "price": 275},
                {"name": "BERRY SOUR", "portion_size": "200 мл", "price": 275},
            ],
            "MIXDRINK": [
                {"name": "GIN&TONIC", "portion_size": "150 мл", "price": 190},
                {"name": "CAPTAIN COLA", "portion_size": "150 мл", "price": 190},
                {"name": "CAPTAIN PINEAPPLE", "portion_size": "150 мл", "price": 190},
                {"name": "SLICED APPLE& LEMONADE", "portion_size": "150 мл", "price": 190},
                {"name": "JACK COLA", "portion_size": "150 мл", "price": 190},
                {"name": "RED COLA", "portion_size": "150 мл", "price": 190},
                {"name": "BURN-FINLANDIA/JAGERMEISTER/JACK DANIELS", "portion_size": "150 мл", "price": 190},
                {"name": "BAILEYS COFFEE", "portion_size": "150 мл", "price": 190},
                {"name": "JAGERMEISTER & TONIC", "portion_size": "150 мл", "price": 190},
                {"name": "CHERRY WHISPERS", "portion_size": "150 мл", "price": 190},
                {"name": "BRANDY-COLA", "portion_size": "150 мл", "price": 190},
                {"name": "FRENCH COLA", "portion_size": "150 мл", "price": 190},
                {"name": "PUR PUR", "portion_size": "150 мл", "price": 190},
                {"name": "SICILIAN LEMON TONIC", "portion_size": "150 мл", "price": 190},
                {"name": "KOSKENKORVA & MAGIC JUICE", "portion_size": "150 мл", "price": 190},
                {"name": "TEQUILA TONIC", "portion_size": "150 мл", "price": 190},
            ],
            "CLASSIC COCKTAILS": [
                {"name": "KEY SOUR", "portion_size": "450 мл", "price": 250},
                {"name": "GAMONDI SPRITZ", "portion_size": "250 мл", "price": 275},
                {"name": "LONG ISLAND", "portion_size": "250 мл", "price": 275},
                {"name": "BOULEVARDIER", "portion_size": "100 мл", "price": 275},
                {"name": "MAI TAI", "portion_size": "250 мл", "price": 250},
                {"name": "MOJITO", "portion_size": "220 мл", "price": 275},
                {"name": "OLD FASHIONED", "portion_size": "100 мл", "price": 250},
                {"name": "NEURONS", "portion_size": "100 мл", "price": 250},
            ],
            "GORDON'S COCKTAILS": [
                {"name": "GORDON'S PORN STAR MARTINI", "portion_size": "200 мл", "price": 225},
                {"name": "TROPIC BASIL SMASH", "portion_size": "200 мл", "price": 225},
                {"name": "PASSION CLOVER CLUB ", "portion_size": "200 мл", "price": 225},
                {"name": "GORDON'S PASSION GIN& TONIC", "portion_size": "200 мл", "price": 225},
                {"name": "PINK SPRITZ", "portion_size": "200 мл", "price": 225},
                {"name": "RASPBERRY HIGHBALL", "portion_size": "200 мл", "price": 225},
            ],
            "FINLANDIA COCKTAILS": [
                {"name": "FINTROPIC ", "portion_size": "160 мл", "price": 190},
                {"name": "FINTONIC  ", "portion_size": "160 мл", "price": 190},
                {"name": "MINT SPRITZ ", "portion_size": "160 мл", "price": 190},
                {"name": "ROSE ", "portion_size": "160 мл", "price": 190},
                {"name": "SPRITZ ", "portion_size": "160 мл", "price": 190},
            ],
            "JACK DANIEL'S COCKTAILS": [
                {"name": "JACK HONEY SMASH", "portion_size": "180 мл", "price": 225},
                {"name": "LYNCHBURG LEMONADE", "portion_size": "180 мл", "price": 225},
                {"name": "ACK APPLE TONIC", "portion_size": "180 мл", "price": 225},
            ],
            "NON ALCOHOL": [
                {"name": "ROOIBOS LEMONADE", "portion_size": "250 мл", "price": 150},
                {"name": "GREEN APPLE LEMONADE", "portion_size": "250 мл", "price": 150},
                {"name": "CITRUS LEMONADE", "portion_size": "250 мл", "price": 150},
                {"name": "COCONUT LEMONADE", "portion_size": "250 мл", "price": 150},
                {"name": "MOJITO", "portion_size": "250 мл", "price": 150},
                {"name": "ICED TEA", "portion_size": "250 мл", "price": 150},
            ],
            "SAN MARE SPARKLING WINE": [
                {"name": "SAN MARE ‹PROSECCO DOC FRIZZANTE", "portion_size": "750 мл", "price": 1000},
                {"name": "SAN	MARE «PROSECCO DOC SPUMANTE»", "portion_size": "750 мл", "price": 1150},
                {"name": "SAN MARE LAMBRUSCO DELL'EMILIA ‹BIANCO›", "portion_size": "750 мл", "price": 700},
                {"name": "SAN MARE LAMBRUGCO DELL'EMILIA ‹•ROSSO›", "portion_size": "750 мл", "price": 700},
                {"name": "SAN MARE FRAGOLINO", "portion_size": "750 мл", "price": 700},
            ],
            "SPARKLING WINE": [
                {"name": "ARTE LATINO CAVA BRUT ", "portion_size": "750 мл", "price": 1000},
            ],
            "CHAMPAGNE": [
                {"name": "MOËT & CHANDON IMPÉRIAL", "portion_size": "750 мл", "price": 3500},
            ],
            "WINES": [
                {"name": "SETTESOLI PINOT GRIGIO", "portion_size": "750 мл", "price": 1000},
                {"name": "FRONTERA “SAUVIGNON BLANC", "portion_size": "750 мл", "price": 900},
                {"name": "EL COTO RIOJA BLANCO", "portion_size": "750 мл", "price": 900},
                {"name": "DOURTHE “BORDEAUX BLAN", "portion_size": "750 мл", "price": 1450},
                {"name": "CANTINA DI NEGRAR VALPOLICELLA", "portion_size": "750 мл", "price": 1050},
                {"name": "DOURTHE “BORDEAUX ROUGE N1", "portion_size": "750 мл", "price": 1450},
                {"name": "PIERRE CHAINIER «ROSE D’ANJOU", "portion_size": "750 мл", "price": 900},
            ],
            "SCOTCH WHISKY": [
                {"name": "JOHNNIE WALKER RED LABEL", "portion_size": "40 мл", "price": 140},
                {"name": "JOHNNIE WALKER BLACK LABEL 12 Y.O", "portion_size": "40 мл", "price": 210},
                {"name": "COPPER DOG", "portion_size": "40 мл", "price": 190},
                {"name": "THE SINGLETON OF DUFFTOWN 12 YO", "portion_size": "40 мл", "price": 280},
                {"name": "NAKED MALT", "portion_size": "40 мл", "price": 190},
                {"name": "TALISKER 1O YO", "portion_size": "40 мл", "price": 300},
                {"name": "GLENMORANGIE THE ORIGINAL, 10 YO", "portion_size": "40 мл", "price": 3000},
                {"name": "THE MACALLAN TRIPLE CASE 12 YO", "portion_size": "40 мл", "price": 350},
            ],
            "BOURBON WHISKEY": [
                {"name": "BULLEIT BOURBON", "portion_size": "40 мл", "price": 200},
                {"name": "BULLEIT RYE", "portion_size": "40 мл", "price": 200},
                {"name": "WOODFORD RESERVE", "portion_size": "40 мл", "price": 200},
                {"name": "WOODFORD RESERVE RYE", "portion_size": "40 мл", "price": 200},
            ],
            "TENNESSEE WHISKEY": [
                {"name": "JACK DANIELS OLD  №7", "portion_size": "40 мл", "price": 150},
                {"name": "JACK DANIEL S TENNESSEE HONEY", "portion_size": "40 мл", "price": 150},
                {"name": "JACK DANIEL S TENNESSEE APPLE", "portion_size": "40 мл", "price": 150},
                {"name": "JACK DANIEL S TENNESSEE FIRE", "portion_size": "40 мл", "price": 150},
                {"name": "JACK DANIEL S GENTLEMAN JACK", "portion_size": "40 мл", "price": 200},
                {"name": "JACK DANIEL S SINGLE BARREL", "portion_size": "40 мл", "price": 250},
            ],
            "IRISH WHISKEY": [
                {"name": "ROE & CO", "portion_size": "40 мл", "price": 200},
                {"name": "O'BRIAN", "portion_size": "40 мл", "price": 150},
            ],
            "GIN": [
                {"name": "GORDON'S LONDON DRY", "portion_size": "40 мл", "price": 120},
                {"name": "GORDON'S PREMIUM PINK", "portion_size": "40 мл", "price": 120},
                {"name": "GORDON'S TROPICAL PASSIONFRUIT", "portion_size": "40 мл", "price": 120},
                {"name": "GORDON'S SICILIAN LEMON", "portion_size": "40 мл", "price": 120},
                {"name": "TANQUERAY №TEN", "portion_size": "40 мл", "price": 240},
                {"name": "TANQUERAY FLOR DE SEVILLA", "portion_size": "40 мл", "price": 140},
            ],
            "TEQUILA": [
                {"name": "JARANA BLANCO 1O0° BLUE AGAVE", "portion_size": "40 мл", "price": 140},
                {"name": "JARANA REPOSADO 1O0° BLUE AGAVE", "portion_size": "40 мл", "price": 140},
                {"name": "EL JIMADOR BLANCO 10O° AGAVE", "portion_size": "40 мл", "price": 140},
                {"name": "EL JIMADOR REPOSADO 1OO° AGAVE", "portion_size": "40 мл", "price": 140},
                {"name": "DON JULIO REPOSADO", "portion_size": "40 мл", "price": 350},
            ],
            "ROM": [
                {"name": "CAPTAIN MORGAN ORIGINAL SPICED GOLD", "portion_size": "40 мл", "price": 120},
                {"name": "CAPTAIN MORGAN WHITE", "portion_size": "40 мл", "price": 120},
                {"name": "CAPTAIN MORGAN DARK", "portion_size": "40 мл", "price": 120},
                {"name": "CAPTAIN MORGAN BLACK SPICED", "portion_size": "40 мл", "price": 120},
                {"name": "RON SANTIAGO DE CUBA ANEJO", "portion_size": "40 мл", "price": 120},
                {"name": "ZACAPA SOLERA GRAN RESERVA", "portion_size": "40 мл", "price": 350},
            ],
            "COGNAC": [
                {"name": "HENNESSY VERY SPECIAL", "portion_size": "40 мл", "price": 270},
                {"name": "HENNESSY VSOP", "portion_size": "40 мл", "price": 350},
                {"name": "REMY  MARTIN VSOP", "portion_size": "40 мл", "price": 350},
            ],
            "BRANDY": [
                {"name": "SAINT REMY XO", "portion_size": "40 мл", "price": 155},
                {"name": "METAXA 5 STARS", "portion_size": "40 мл", "price": 155},
            ],
            "VODKA FROM A VILLAGE": [
                {"name": "KOSKENKORVA", "portion_size": "40 мл", "price": 90},
                {"name": "KOSKENKORVA GINGER", "portion_size": "40 мл", "price": 90},
                {"name": "KOSKENKORVA PASSIONFRUIT", "portion_size": "40 мл", "price": 90},
                {"name": "KOSKENKORVA BLUEBERRY JUNIPER", "portion_size": "40 мл", "price": 90},
                {"name": "KOSKENKORVA ESPRESSO", "portion_size": "40 мл", "price": 90},
                {"name": "KOSKENKORVA LEMON LIME YARROW", "portion_size": "40 мл", "price": 90},
                {"name": "KOSKENKORVA APPLE", "portion_size": "40 мл", "price": 90},
            ],
            "VODKA": [
                {"name": "KRADA PREMIUM CLASSIC", "portion_size": "40 мл", "price": 70},
                {"name": "SMIRNOFF RED №21", "portion_size": "40 мл", "price": 100},
                {"name": "BELVEDERE", "portion_size": "40 мл", "price": 180},
            ],
            "FINLANDIA VODKA": [
                {"name": "FINLANOIA  CLASSIC", "portion_size": "40 мл", "price": 90},
                {"name": "FINLANDIA CRANBERRY", "portion_size": "40 мл", "price": 90},
                {"name": "FINLANDIA GRAPEFRUIT", "portion_size": "40 мл", "price": 90},
                {"name": "FINLANDIA COCONUT", "portion_size": "40 мл", "price": 90},
                {"name": "FINLANDIA REDBERRY", "portion_size": "40 мл", "price": 90},
                {"name": "FINLANDIA BLACKCURRANT", "portion_size": "40 мл", "price": 90},
                {"name": "FINLANDIA LIME", "portion_size": "40 мл", "price": 90},
                {"name": "FINLANDIA BOTANICAL CUCUMBER & MINT", "portion_size": "40 мл", "price": 90},
                {"name": "FINLANDIA BOTANICAL WILBERRY & ROSE", "portion_size": "40 мл", "price": 90},
            ],
            "VERMOUTH": [
                {"name": "GAMONDI VERMOUTH BIANCO DI TORINO", "portion_size": "40 мл", "price": 80},
                {"name": "GAMONDI VERMOUTH ROSSO DI TORINO", "portion_size": "40 мл", "price": 80},
                {"name": "TOSO VERMOUTH EXTRA DRY", "portion_size": "40 мл", "price": 80},
            ],
            "ICE COLD SHOT": [
                {"name": "JÄGERMEISTER", "portion_size": "40 мл", "price": 100},
            ],
            "ABSENT": [
                {"name": "XENTA ABSENTA", "portion_size": "40 мл", "price": 130},
            ],
            "LIQUOR": [
                {"name": "BAILEYS THE ORIGINAL", "portion_size": "40 мл", "price": 120},
                {"name": "BAILEYS SALTED CARAMEL", "portion_size": "40 мл", "price": 100},
                {"name": "SAMBUCA ANTICA CLASSIC", "portion_size": "40 мл", "price": 120},
                {"name": "COINTREAU", "portion_size": "40 мл", "price": 120},
                {"name": "RIGA BLACK BALSAM CURRANT", "portion_size": "40 мл", "price": 120},
                {"name": "RIGA BLACK CHERRY", "portion_size": "40 мл", "price": 100},
                {"name": "CHERRY TEMPTATION", "portion_size": "40 мл", "price": 100},
                {"name": "GAMONDI APERETIVO", "portion_size": "40 мл", "price": 90},
                {"name": "GAMOND[ BITTER", "portion_size": "40 мл", "price": 90},
            ],
            "BEER": [
                {"name": "CORONA EXTRA", "portion_size": "330 мл", "price": 160},
                {"name": "CARLSBERG", "portion_size": "500 мл", "price": 100},
                {"name": "KRONENBOURG 1664 BLANC", "portion_size": "500 мл", "price": 120},
                {"name": "CARLSBERG NA", "portion_size": "500 мл", "price": 120},
            ],
            "COLD DRINKS": [
                {"name": "COCA-COLA", "portion_size": "250 мл", "price": 80},
                {"name": "COCA-COLA ZERO", "portion_size": "250 мл", "price": 80},
                {"name": "FANTA, SPRITE, SCHWEPPES INDIAN TONIC", "portion_size": "250 мл", "price": 80},
                {"name": "BURN ORIGINAL", "portion_size": "250 мл", "price": 120},
                {"name": "RICH IN ASSORTMENT", "portion_size": "250 мл", "price": 80},
                {"name": "BONAQUA", "portion_size": "250 мл", "price": 80},
                {"name": "МОРШИНСЬКА", "portion_size": "250 мл", "price": 80},
                {"name": "EVIAN", "portion_size": "250 мл", "price": 120},
                {"name": "EVIAN", "portion_size": "750 мл", "price": 199},
            ],
            "COFFEE": [
                {"name": "ESPRESSO", "portion_size": "30 мл", "price": 70},
                {"name": "AMERICANO", "portion_size": "60 мл", "price": 70},
                {"name": "DOPPIO", "portion_size": "60 мл", "price": 80},
                {"name": "CAPUCHINO", "portion_size": "130 мл", "price": 90},
                {"name": "LATTE", "portion_size": "180 мл", "price": 100},
                {"name": "ICE COFFEE", "portion_size": "150 мл", "price": 120},
                {"name": "ESPRESSO ORANGE", "portion_size": "150 мл", "price": 120},
                {"name": "ESPRESSO TONIC", "portion_size": "150 мл", "price": 120},
                {"name": "МОЛОКО", "portion_size": "50 мл", "price": 20},
                {"name": "МОЛОКО МИГДАЛЕВЕ/СОЄВЕ", "portion_size": "50 мл", "price": 50},
            ],


        }

        for category_name, products in products_data.items():
            category, created = Category.objects.get_or_create(name=category_name)
            for product_data in products:
                Product.objects.get_or_create(
                    category=category,
                    name=product_data["name"],
                    portion_size=product_data["portion_size"],
                    price=product_data["price"],
                )

        self.stdout.write(self.style.SUCCESS('Successfully populated the database.'))

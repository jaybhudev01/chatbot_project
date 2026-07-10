def panchang():

    # 1. The Questions Dataset (List of valid query keys)
    july_2026_questions = [
        "2026-07-01", "2026-07-02", "2026-07-03", "2026-07-04", "2026-07-05",
        "2026-07-06", "2026-07-07", "2026-07-08", "2026-07-09", "2026-07-10",
        "2026-07-11", "2026-07-12", "2026-07-13", "2026-07-14", "2026-07-15",
        "2026-07-16", "2026-07-17", "2026-07-18", "2026-07-19", "2026-07-20",
        "2026-07-21", "2026-07-22", "2026-07-23", "2026-07-24", "2026-07-25",
        "2026-07-26", "2026-07-27", "2026-07-28", "2026-07-29", "2026-07-30",
        "2026-07-31"
    ]

    # 2. The Answers Dataset (Dictionary for instant response retrieval)
    july_2026_answers = {
        "2026-07-01": "On 2026-07-01 (Wednesday), it is Ashadha Krishna Pratipada during the Krishna Paksha.",
        "2026-07-02": "On 2026-07-02 (Thursday), it is Ashadha Krishna Dwitiya during the Krishna Paksha.",
        "2026-07-03": "On 2026-07-03 (Friday), it is Ashadha Krishna Tritiya (Krishna Paksha). Today we celebrate Sankashti Chaturthi!",
        "2026-07-04": "On 2026-07-04 (Saturday), it is Ashadha Krishna Chaturthi during the Krishna Paksha.",
        "2026-07-05": "On 2026-07-05 (Sunday), it is Ashadha Krishna Panchami during the Krishna Paksha.",
        "2026-07-06": "On 2026-07-06 (Monday), it is Ashadha Krishna Shashthi during the Krishna Paksha.",
        "2026-07-07": "On 2026-07-07 (Tuesday), it is Ashadha Krishna Saptami (Krishna Paksha). Today is Kalashtami.",
        "2026-07-08": "On 2026-07-08 (Wednesday), it is Ashadha Krishna Ashtami during the Krishna Paksha.",
        "2026-07-09": "On 2026-07-09 (Thursday), it is Ashadha Krishna Navami during the Krishna Paksha.",
        "2026-07-10": "On 2026-07-10 (Friday), it is Ashadha Krishna Dashami (Krishna Paksha). Today is Yogini Ekadashi!",
        "2026-07-11": "On 2026-07-11 (Saturday), it is Ashadha Krishna Ekadashi (Krishna Paksha). Today is Gauna Ekadashi.",
        "2026-07-12": "On 2026-07-12 (Sunday), it is Ashadha Krishna Dwadashi (Krishna Paksha). Today is Masik Shivratri and Pradosh Vrat.",
        "2026-07-13": "On 2026-07-13 (Monday), it is Ashadha Krishna Trayodashi during the Krishna Paksha.",
        "2026-07-14": "On 2026-07-14 (Tuesday), it is Ashadha Amavasya (Krishna Paksha). Today is Darsha Amavasya.",
        "2026-07-15": "On 2026-07-15 (Wednesday), it is Ashadha Shukla Pratipada (Shukla Paksha). The auspicious Gupta Navratri Begins today!",
        "2026-07-16": "On 2026-07-16 (Thursday), it is Ashadha Shukla Dwitiya (Shukla Paksha). Today marks the Jagannath Rath Yatra and Karka Sankranti.",
        "2026-07-17": "On 2026-07-17 (Friday), it is Ashadha Shukla Tritiya (Shukla Paksha). Today is Varad Chaturthi.",
        "2026-07-18": "On 2026-07-18 (Saturday), it is Ashadha Shukla Chaturthi during the Shukla Paksha.",
        "2026-07-19": "On 2026-07-19 (Sunday), it is Ashadha Shukla Panchami (Shukla Paksha). Today is Skanda Sashti.",
        "2026-07-20": "On 2026-07-20 (Monday), it is Ashadha Shukla Shashthi during the Shukla Paksha.",
        "2026-07-21": "On 2026-07-21 (Tuesday), it is Ashadha Shukla Saptami (Shukla Paksha). Today is Parvati Jayanti and Durga Ashtami.",
        "2026-07-22": "On 2026-07-22 (Wednesday), it is Ashadha Shukla Ashtami (Shukla Paksha). Today is Bhadli Navami.",
        "2026-07-23": "On 2026-07-23 (Thursday), it is Ashadha Shukla Navami during the Shukla Paksha.",
        "2026-07-24": "On 2026-07-24 (Friday), it is Ashadha Shukla Dashami (Shukla Paksha). Today is Asha Dashami Vrat.",
        "2026-07-25": "On 2026-07-25 (Saturday), it is Ashadha Shukla Ekadashi (Shukla Paksha). Today is Devshayani Ekadashi and Chaturmas Begins.",
        "2026-07-26": "On 2026-07-26 (Sunday), it is Ashadha Shukla Dwadashi (Shukla Paksha). Today is Ravi Pradosh Vrat.",
        "2026-07-27": "On 2026-07-27 (Monday), it is Ashadha Shukla Trayodashi (Shukla Paksha). Jaya Parvati Vrat Begins today.",
        "2026-07-28": "On 2026-07-28 (Tuesday), it is Ashadha Shukla Chaturdashi (Shukla Paksha). Today is Kokila Vrat.",
        "2026-07-29": "On 2026-07-29 (Wednesday), it is Ashadha Purnima (Shukla Paksha). Today is the highly auspicious Guru Purnima and Vyasa Puja!",
        "2026-07-30": "On 2026-07-30 (Thursday), it is Shravana Krishna Pratipada (Krishna Paksha). The holy Shravan Month Begins today!",
        "2026-07-31": "On 2026-07-31 (Friday), it is Shravana Krishna Dwitiya during the Krishna Paksha."
    }
    return july_2026_answers